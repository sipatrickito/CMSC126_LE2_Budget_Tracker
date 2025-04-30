from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Budget, Entry


class BootstrapFormMixin(forms.Form):
    def full_clean(self):
        super().full_clean()
        for name, field in self.fields.items():
            if name in self.errors:
                field.widget.attrs["class"] += " is-invalid"
            else:
                field.widget.attrs["class"] += " is-valid"


class UserRegisterForm(UserCreationForm, BootstrapFormMixin):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class EntryForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Entry
        fields = ["title", "amount", "date", "type", "category", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


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


class BudgetForm(forms.ModelForm, BootstrapFormMixin):
    month_input = forms.DateField(
        input_formats=["%Y-%m"],
        widget=forms.DateInput(attrs={"type": "month"}),
        label="Month",
    )

    class Meta:
        model = Budget
        fields = ["month_input", "category", "amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01"}),
        }
