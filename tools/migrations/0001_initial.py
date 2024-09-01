# Generated by Django 4.2.7 on 2024-09-01 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("topics", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Tool",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, unique=True)),
                ("short_description", models.TextField(blank=True, max_length=50)),
                ("full_description", models.TextField(blank=True, max_length=500)),
                ("instructions", models.TextField(blank=True, max_length=5000)),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "topics",
                    models.ManyToManyField(related_name="tools", to="topics.topic"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
