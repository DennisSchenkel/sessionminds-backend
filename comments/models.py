from django.db import models
from tools.models import Tool


class Comment(models.Model):
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
