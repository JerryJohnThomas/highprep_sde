# Generated by Django 4.1.5 on 2023-01-22 11:02

import algo_apis.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("algo_apis", "0002_algorithmstatusmodel"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="location",
            name="latitude",
        ),
        migrations.RemoveField(
            model_name="location",
            name="longitude",
        ),
        migrations.AddField(
            model_name="location",
            name="location_array",
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name="location",
            name="random_number",
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="location",
            name="username",
            field=models.EmailField(default="rk@gmail.com", max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="algorithmstatusmodel",
            name="excelSheetFile",
            field=models.FileField(
                null=True, upload_to=algo_apis.models.content_file_name
            ),
        ),
        migrations.AlterField(
            model_name="algorithmstatusmodel",
            name="random_number",
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name="location",
            name="location_name",
            field=models.JSONField(null=True),
        ),
    ]
