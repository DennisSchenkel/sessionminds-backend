from django.db import models
from tools.models import Tool
from django.contrib.auth.models import User


class Vote(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(
        Tool, related_name="votes", on_delete=models.CASCADE
        )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        unique_together = ["user", "tool"]

    def __str__(self):
        return f"{self.tool} - {self.user} - {self.created}"
