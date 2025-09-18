from django.db import models


class Module(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    installed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
