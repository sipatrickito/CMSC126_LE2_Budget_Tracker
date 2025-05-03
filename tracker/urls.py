from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import TrackerUserLoginForm

urlpatterns = [
    path("set-budget/", views.set_budget, name="set_budget"),
    path("", views.home, name="home"),
    path("register/", views.TrackerUserCreateView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="user_login.html",
            authentication_form=TrackerUserLoginForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
    path("add/", views.add_entry, name="add_entry"),
    path("edit/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    path("delete/<int:entry_id>/", views.delete_entry, name="delete_entry"),
    path("delete/<int:entry_id>/", views.delete_entry, name="delete_entry"),
    path("export/", views.export_csv, name="export_csv"),
]
