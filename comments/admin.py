from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "tool", "user", "created_at", "updated_at")
    list_filter = ("tool", "user", "created_at", "updated_at")
