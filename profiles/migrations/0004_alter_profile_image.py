# Generated by Django 4.2.14 on 2024-07-29 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_alter_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                default="/anonymdog_ctenaf", upload_to="user-images/"
            ),
        ),
    ]