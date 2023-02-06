# Generated by Django 4.1.5 on 2023-02-06 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("algo_apis", "0014_algorithmstatusmodel_dynamicpickupexcelsheet"),
    ]

    operations = [
        migrations.AddField(
            model_name="algorithmstatusmodel",
            name="number_of_drivers",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="algorithmstatusmodel",
            name="number_of_locations",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="rider",
            name="temp_id",
            field=models.IntegerField(null=True),
        ),
    ]
