from django.contrib import admin
from .models import Tool
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Tool)
class ToolAdmin(SummernoteModelAdmin):
    list_display = ("title", "id", "user", )
