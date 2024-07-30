from django.db import models
from django.contrib.auth.models import User
from categories.models import Category


class Tool(models.Model):
    """
    Represents a tool.

    Attributes:
        title (str): The title of the tool.
        short_description (str): The short description of the tool.
        full_description (str): The full description of the tool.
        categories (ManyToManyField): The categories associated with the tool.
        instructions (str): The instructions for using the tool.
        author (ForeignKey): The author of the tool entry.
        created (datetime): Date and time when the tool was created.
        updated (datetime): Date and time when the tool was last updated.
    """

    title = models.CharField(max_length=100, unique=True)
    short_description = models.TextField(max_length=100, blank=True)
    full_description = models.TextField(max_length=500, blank=True)
    categories = models.ManyToManyField(Category, related_name="tools")
    instructions = models.TextField(max_length=5000, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default="Anonymous"
        )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
