from django.forms import Form as DjForm
from django.forms import ModelForm as DjModelForm


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
