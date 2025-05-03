from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import Form as DjForm
from django.forms import ModelForm as DjModelForm

from .models import Budget, Entry


class BaseForm(DjForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            class_attr = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = ("form-control " + class_attr).strip()

    def invalid_field(self, field):
        field.widget.attrs["class"] += " is-invalid"

    def valid_field(self, field):
        field.widget.attrs["class"] += " is-valid"

    def full_clean(self):
        super().full_clean()
        for name, field in self.fields.items():
            if name in self.errors:
                self.invalid_field(field)


class Form(BaseForm):
    pass


class ModelForm(DjModelForm, BaseForm):
    pass


class TrackerUserCreateForm(UserCreationForm, ModelForm):
    pass


class TrackerUserLoginForm(AuthenticationForm, Form):
    def full_clean(self):
        super().full_clean()
        for name, field in self.fields.items():
            if name in self.errors:
                field.widget.attrs["aria-describedby"] = "tracker-login-form-error"


class EntryForm(ModelForm):
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


class BudgetForm(ModelForm):
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
