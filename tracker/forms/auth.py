from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from tracker.forms import BootstrapFormMixin


class TrackerUserCreateForm(BootstrapFormMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bootstrapfy_fields(self.fields.values())

    def full_clean(self):
        super().full_clean()
        print(self.errors)


class TrackerUserLoginForm(BootstrapFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bootstrapfy_fields(self.fields.values())

    def full_clean(self):
        super().full_clean()
        for name, field in self.fields.items():
            if name in self.errors:
                self.invalid_field(field)
                field.widget.attrs["aria-describedby"] = "tracker-login-form-error"
