from django.db import models
from tools.models import Tool
from django.contrib.auth.models import User


# Vote model
class Vote(models.Model):
    """
    Represents a vote for a tool.

    Args:
        models: The base model class.

    Returns:
        Vote: The vote object.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(
        Tool, related_name="votes", on_delete=models.CASCADE
        )
    created = models.DateTimeField(auto_now_add=True)

    # Ensure that a user can only vote once for a tool
    class Meta:
        ordering = ['-created']
        unique_together = ["user", "tool"]

    def __str__(self):
        return f"{self.tool} - {self.user} - {self.created}"
