from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.utils.dateparse import parse_date
from datetime import date, datetime
import json
import csv
from django.http import HttpResponse
from .models import Entry
from .models import Entry, Category, Budget
from .forms import UserRegisterForm, EntryForm, BudgetForm


@login_required
def home(request):
    current_date = date.today()
    selected_month = request.GET.get('month')

    if selected_month:
        year, month = map(int, selected_month.split('-'))
    else:
        year = current_date.year
        month = current_date.month

    entries = Entry.objects.filter(user=request.user, date__year=year, date__month=month)

    total_income = entries.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = entries.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses

    monthly_summary = Entry.objects.filter(user=request.user) \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(
            total_income=Sum('amount', filter=Q(type='income')),
            total_expenses=Sum('amount', filter=Q(type='expense'))
        ).order_by('month')

    expenses_by_category = entries.filter(type='expense').values('category__name', 'category').annotate(total=Sum('amount'))

    category_expenses = []
    category_totals = []
    for expense in expenses_by_category:
        category_expenses.append({
            'name': expense['category__name'],
            'total': float(expense['total'])
        })
        category_totals.append({
            'category': expense['category'],
            'total_spent': expense['total']
        })

    pie_chart_data = {
        'labels': [expense['name'] for expense in category_expenses],
        'data': [expense['total'] for expense in category_expenses],
    }

    budgets = Budget.objects.filter(user=request.user, month=month, year=year).select_related('category')

    category_spending = {cat['category']: cat['total'] for cat in expenses_by_category}

    budget_warnings = {}
    for budget in budgets:
        spent = category_spending.get(budget.category.id, 0)
        over = spent > budget.amount
        budget_warnings[budget.category.id] = {
            'category_name': budget.category.name,
            'budget': budget.amount,
            'spent': spent,
            'over': over
        }

    categories = Category.objects.all()
    context = {
        'today': current_date,
        'month_summary': {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance,
        },
        'entries': entries,
        'pie_chart_data': json.dumps(pie_chart_data),
        'monthly_summary': list(monthly_summary),
        'budget_warnings': budget_warnings,
        'selected_month': month,
        'selected_year': year,
        'categories': categories,
    }

    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def add_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Entry added successfully!')
            return redirect('home')
    else:
        form = EntryForm()
    return render(request, 'add_entry.html', {'form': form})


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated successfully!')
            return redirect('home')
    else:
        form = EntryForm(instance=entry)
    return render(request, 'edit_entry.html', {'form': form})


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted successfully!')
        return redirect('home')
    return render(request, 'confirm_delete.html', {'entry': entry})


@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user

            month_date = form.cleaned_data['month_input']
            budget.month = month_date.month
            budget.year = month_date.year

            existing = Budget.objects.filter(
                user=request.user,
                month=budget.month,
                year=budget.year,
                category=budget.category
            ).first()

            if existing:
                existing.amount = budget.amount
                existing.save()
            else:
                budget.save()

            messages.success(request, 'Budget saved successfully.')
            return redirect('home')
    else:
        form = BudgetForm()

    return render(request, 'set_budget.html', {'form': form})

@login_required
def export_csv(request):
    # Optional filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')

    entries = Entry.objects.filter(user=request.user)

    if start_date:
        entries = entries.filter(date__gte=start_date)
    if end_date:
        entries = entries.filter(date__lte=end_date)
    if category:
        entries = entries.filter(category_id=category)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="budget_entries.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Title', 'Type', 'Category', 'Amount'])

    for entry in entries:
        writer.writerow([entry.date, entry.title, entry.get_type_display(), entry.category.name, entry.amount])

    return response
