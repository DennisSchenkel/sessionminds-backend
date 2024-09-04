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
    id = models.AutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=100)
    icon_code = models.CharField(unique=True, max_length=10)

    def __str__(self):
        return self.title


class Topic(models.Model):
    """
    Represents a topic.

    Attributes:
        title (str): The title of the topic.
        description (str): The description of the topic.
        icon (Icon): The icon associated with the topic.
        slug (str): The slug for the topic.
        created (datetime): Date and time when the topic was created.
        updated (datetime): Date and time when the topic was last updated.
    """

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=50, blank=True)
    icon = models.ForeignKey(
        Icon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
        )
    slug = models.SlugField(unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def tool_count(self):
        return self.tools.count()

    def __str__(self):
        return self.title
