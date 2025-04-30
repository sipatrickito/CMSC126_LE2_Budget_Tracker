from django.contrib import auth as dj_auth
from django.urls import path

from .forms.auth import TrackerUserLoginForm
from .views import auth as tr_auth

# from .views import track

urlpatterns = [
    # -------------------- Auth paths --------------------
    path(
        "register/",
        tr_auth.TrackerUserCreateView.as_view(),
        name="register_tracker_user",
    ),
    path(
        "",
        dj_auth.views.LoginView.as_view(
            template_name="user_login.html",
            authentication_form=TrackerUserLoginForm,
        ),
        name="login_tracker_user",
    ),
    path("logout/", dj_auth.views.LogoutView.as_view(), name="logout_tracker_user"),
    # -------------------- Tracker paths --------------------
]
