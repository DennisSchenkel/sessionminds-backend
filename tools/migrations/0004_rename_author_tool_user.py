# Generated by Django 4.2.14 on 2024-07-30 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tools", "0003_alter_tool_author"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tool",
            old_name="author",
            new_name="user",
        ),
    ]
