from django.contrib import admin
from .models import Vote
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Vote)
class ProfileAdmin(SummernoteModelAdmin):
    list_display = ("id", "user", "tool", "created")
