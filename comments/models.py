from django.db import models
from tools.models import Tool


# Comment model
class Comment(models.Model):
    """
    Represents a comment for a tool.

    Args:
        models: The base model class.

    Returns:
        Comment: The comment object.

    Attributes:
        text (TextField): The comment text.
        tool (ForeignKey): The tool associated with the comment.
        user (ForeignKey): The user who created the comment.
        created_at (DateTimeField): The date and time the comment was created.
        updated_at (DateTimeField): The date and time the comment was updated.
    """
    text = models.TextField()
    tool = models.ForeignKey(
        Tool, on_delete=models.CASCADE, related_name="comments"
        )
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="comments"
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
