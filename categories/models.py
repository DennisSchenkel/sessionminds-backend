from django.db import models
from django.utils.text import slugify


class Icon(models.Model):
    """
    Represents an icon.

    Attributes:
        title (str): The title of the icon.
        icon_code (str): The code representing the icon.

    Methods:
        __str__(): Returns the title of the icon.

    """
    title = models.CharField(unique=True, max_length=100)
    icon_code = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Represents a category.

    Attributes:
        title (str): The title of the category.
        description (str): The description of the category.
        icon (Icon): The icon associated with the category.
        slug (str): The slug for the category.
        created (datetime): Date and time when the category was created.
        updated (datetime): Date and time when the category was last updated.
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
