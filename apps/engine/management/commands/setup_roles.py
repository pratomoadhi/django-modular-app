from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = (
        "Create groups manager, user, public and assign basic permissions for product"
    )

    def handle(self, *args, **kwargs):
        # Import product model dynamically to avoid errors if module not installed
        try:
            from modules.product.models import Product
        except Exception:
            Product = None

        manager, _ = Group.objects.get_or_create(name="manager")
        user, _ = Group.objects.get_or_create(name="user")
        public, _ = Group.objects.get_or_create(name="public")

        if Product:
            ct = ContentType.objects.get_for_model(Product)
            perms = Permission.objects.filter(content_type=ct)
            # manager = add, change, delete, view
            manager.permissions.set(perms)
            # user = add, change, view
            allow = perms.filter(
                codename__in=["add_product", "change_product", "view_product"]
            )
            user.permissions.set(allow)
            # public = view only
            view_perm = perms.filter(codename="view_product")
            public.permissions.set(view_perm)
            self.stdout.write(
                self.style.SUCCESS(
                    "Groups created and assigned permissions for Product."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Product model not importable. Groups created without permissions."
                )
            )
