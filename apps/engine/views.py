import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.management import call_command
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Module


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseForbidden(
                "You do not have permission to access this page."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped


def module_exists(slug):
    base = os.path.join(settings.BASE_DIR, "modules", slug)
    return os.path.isdir(base)


@superuser_required
def module_index(request):
    modules = Module.objects.all()
    return render(request, "engine/index.html", {"modules": modules})


def module_action(request, slug, op):
    """
    op: 'install', 'upgrade', 'uninstall'
    install/upgrade: makemigrations + migrate
    uninstall: migrate <app_label> zero
    """
    module = get_object_or_404(Module, slug=slug)

    if not module_exists(slug):
        messages.error(
            request,
            f"Module folder for '{slug}' not found.",
            extra_tags="module-page-message",
        )
        return redirect(reverse("engine:index"))

    try:
        app_label = slug
        if op in ("install", "upgrade"):
            call_command("makemigrations", app_label)
            call_command("migrate", app_label)
            module.installed = True
            module.save()
            messages.success(
                request,
                f"{op.capitalize()} succeeded for {module.name}",
                extra_tags="module-page-message",
            )
        elif op == "uninstall":
            call_command("migrate", app_label, "zero")
            module.installed = False
            module.save()
            messages.success(
                request,
                f"{module.name} successfully uninstalled",
                extra_tags="module-page-message",
            )
        else:
            messages.error(
                request, "Unknown operation.", extra_tags="module-page-message"
            )
    except Exception as e:
        messages.error(request, f"Error: {e}", extra_tags="module-page-message")

    return redirect(reverse("engine:index"))


class CustomLoginView(LoginView):
    template_name = "auth/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect("engine:index")
            else:
                return redirect("product:landing")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy("engine:index")  # /module/
        return reverse_lazy("product:landing")  # /product/
