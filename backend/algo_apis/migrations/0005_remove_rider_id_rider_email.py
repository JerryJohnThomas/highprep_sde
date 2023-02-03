# Generated by Django 4.1.5 on 2023-01-22 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("algo_apis", "0004_remove_location_location_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rider",
            name="id",
        ),
        migrations.AddField(
            model_name="rider",
            name="email",
            field=models.EmailField(
                default="1@gmail.com", max_length=254, primary_key=True, serialize=False
            ),
        ),
    ]