from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from tracker.forms.auth import TrackerUserCreateForm


class TrackerUserCreateView(View):
    def get(self, request, *args, **kwargs):
        if request.GET:
            form = TrackerUserCreateForm(request.GET)
            taken = "username" in form.errors
            return JsonResponse(
                {
                    "taken": taken,
                    "message": form.errors["username"][0] if taken else None,
                }
            )

        return render(request, "user_register.html", {"form": TrackerUserCreateForm()})

    def post(self, request, *args, **kwargs):
        form = TrackerUserCreateForm(request.POST)
        if not form.is_valid():
            return render(request, "user_register.html", {"form": form}, status=400)
        form.save()

        return redirect("login_tracker_user")
