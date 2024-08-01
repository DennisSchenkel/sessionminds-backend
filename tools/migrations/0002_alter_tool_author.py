# Generated by Django 4.2.14 on 2024-07-30 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tools", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tool",
            name="author",
            field=models.ForeignKey(
                default="Anonymous",
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="tools",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]