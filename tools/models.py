from django.db import models
from django.contrib.auth.models import User
from topics.models import Topic
from django.utils.text import slugify


class Tool(models.Model):
    """
    Represents a tool.

    Attributes:
        title (str): The title of the tool.
        short_description (str): The short description of the tool.
        full_description (str): The full description of the tool.
        topics (ManyToManyField): The topics associated with the tool.
        instructions (str): The instructions for using the tool.
        user (ForeignKey): The author of the tool entry.
        created (datetime): Date and time when the tool was created.
        updated (datetime): Date and time when the tool was last updated.
    """

    title = models.CharField(max_length=100, unique=True)
    short_description = models.TextField(max_length=50, blank=False)
    full_description = models.TextField(max_length=500, blank=False)
    topics = models.ManyToManyField(Topic, related_name="tools")
    instructions = models.TextField(max_length=5000, blank=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1,
        )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
