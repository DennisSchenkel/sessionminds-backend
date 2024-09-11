from django.contrib import admin
from .models import Topic, Icon
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Topic)
class TopicAdmin(SummernoteModelAdmin):
    list_display = ("id", "title")


admin.site.register(Icon)
