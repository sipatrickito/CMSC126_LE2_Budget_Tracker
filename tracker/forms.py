from django import forms
from .models import Budget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

from .models import Entry, Category

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'amount', 'date', 'type', 'category', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

# class BudgetForm(forms.ModelForm):
#     class Meta:
#         model = Budget
#         fields = ['month', 'category', 'amount']
#         widgets = {
#             'month': forms.DateInput(attrs={'type': 'month'}),
#         }

# class BudgetForm(forms.ModelForm):
#     class Meta:
#         model = Budget
#         fields = ['category', 'month', 'year', 'amount']
#         widgets = {
#             'amount': forms.NumberInput(attrs={'step': '0.01'}),
#         }

class BudgetForm(forms.ModelForm):
    month_input = forms.DateField(
        input_formats=['%Y-%m'],
        widget=forms.DateInput(attrs={'type': 'month'}),
        label='Month'
    )

    class Meta:
        model = Budget
        fields = ['month_input', 'category', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }