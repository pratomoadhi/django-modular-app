from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
