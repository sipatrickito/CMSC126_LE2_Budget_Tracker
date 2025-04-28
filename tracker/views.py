from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, EntryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Entry, Category
from django.db.models import Sum
from datetime import date
import json 
from . import models
from django.db.models import Q
from django.db.models.functions import TruncMonth

@login_required
def home(request):
    # current_date = date.today()

    # entries = Entry.objects.filter(user=request.user, date__month=current_date.month, date__year=current_date.year)

    current_date = date.today()

    selected_month = request.GET.get('month')

    if selected_month:
        year, month = map(int, selected_month.split('-'))
        entries = Entry.objects.filter(user=request.user, date__year=year, date__month=month)
    else:
        entries = Entry.objects.filter(user=request.user, date__year=current_date.year, date__month=current_date.month)

    total_income = Sum('amount', filter=Q(type='income'))
    total_expenses = Sum('amount', filter=Q(type='expense'))

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



    expenses_by_category = entries.filter(type='expense').values('category__name').annotate(total=Sum('amount'))

    category_expenses = []
    for expense in expenses_by_category:
        category_expenses.append({
            'name': expense['category__name'],
            'total': float(expense['total'])  
        })

    pie_chart_data = {
        'labels': [expense['name'] for expense in category_expenses],
        'data': [expense['total'] for expense in category_expenses],
    }

    month_summary = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
    }

    return render(
        request, 
        'home.html', 
        {
            'today': date.today(),
            'month_summary': month_summary,
            'entries': entries,
            'pie_chart_data': json.dumps(pie_chart_data),
            'monthly_summary': list(monthly_summary)
        }
    )

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
