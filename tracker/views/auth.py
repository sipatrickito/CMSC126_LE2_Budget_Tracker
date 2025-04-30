from django.shortcuts import redirect, render
from django.views.generic import View

from tracker.forms.auth import TrackerUserCreateForm


class TrackerUserCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, "user_register.html", {"form": TrackerUserCreateForm()}
        )

    def post(self, request, *args, **kwargs):
        form = TrackerUserCreateForm(request.POST)
        if not form.is_valid():
            return render(request, "user_register.html", {"form": form}, status=400)
        form.save()

        return redirect("login_tracker_user")
