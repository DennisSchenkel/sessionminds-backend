from django.db import models
from django.utils.text import slugify


class Icon(models.Model):
    """
    Create a model for icons.
    """
    title = models.CharField(unique=True, max_length=100)
    icon_code = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Create a model for categories.
    """
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    icon = models.ForeignKey(Icon, on_delete=models.SET_DEFAULT, default=1)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
