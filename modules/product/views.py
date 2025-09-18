from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.http import Http404

from .models import Product
from apps.engine.models import Module


def in_group(user, group_name):
    return user.is_authenticated and user.groups.filter(name=group_name).exists()


def manager_required(view_func):
    return user_passes_test(lambda u: in_group(u, "manager"))(view_func)


def user_required(view_func):
    return user_passes_test(lambda u: in_group(u, "user") or in_group(u, "manager"))(
        view_func
    )


def public_view(view_func):
    return view_func


def module_must_be_installed(slug="product"):
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            mod = Module.objects.filter(slug=slug, installed=True).first()
            if not mod:
                raise Http404("Module not found or not installed.")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


@public_view
@module_must_be_installed("product")
def landing(request):
    products = Product.objects.all()

    # Flags for template logic
    can_create = in_group(request.user, "manager") or in_group(request.user, "user")
    can_update = can_create
    can_delete = in_group(request.user, "manager")
    can_manage_engine = request.user.is_superuser

    return render(
        request,
        "product/landing.html",
        {
            "products": products,
            "can_create": can_create,
            "can_update": can_update,
            "can_delete": can_delete,
            "can_manage_engine": can_manage_engine,
        },
    )


@user_required
@module_must_be_installed("product")
def product_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        barcode = request.POST.get("barcode")
        price = request.POST.get("price") or 0
        stock = request.POST.get("stock") or 0
        Product.objects.create(name=name, barcode=barcode, price=price, stock=stock)
        messages.success(request, "Product created", extra_tags="product-page-message")
        return redirect(reverse("product:landing"))
    return render(request, "product/form.html")


@user_required
@module_must_be_installed("product")
def product_edit(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        p.name = request.POST.get("name")
        p.barcode = request.POST.get("barcode")
        p.price = request.POST.get("price") or 0
        p.stock = request.POST.get("stock") or 0
        p.save()
        messages.success(request, "Product updated", extra_tags="product-page-message")
        return redirect(reverse("product:landing"))
    return render(request, "product/form.html", {"product": p})


@manager_required
@module_must_be_installed("product")
def product_delete(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        p.delete()
        messages.success(request, "Product deleted", extra_tags="product-page-message")
        return redirect(reverse("product:landing"))
    return render(request, "product/confirm_delete.html", {"product": p})
