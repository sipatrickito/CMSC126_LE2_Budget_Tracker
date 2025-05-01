from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from tracker.forms import Form, ModelForm


class TrackerUserCreateForm(UserCreationForm, ModelForm):
    pass


class TrackerUserLoginForm(AuthenticationForm, Form):
    def full_clean(self):
        super().full_clean()
        for name, field in self.fields.items():
            if name in self.errors:
                field.widget.attrs["aria-describedby"] = "tracker-login-form-error"
