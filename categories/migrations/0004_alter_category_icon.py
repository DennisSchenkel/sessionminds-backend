# Generated by Django 4.2.14 on 2024-07-30 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0003_rename_categorie_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="icon",
            field=models.ForeignKey(
                default="U+2716",
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="categories.icon",
            ),
        ),
    ]
