# Generated by Django 4.1.7 on 2023-12-18 17:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_request", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="datarequest",
            name="rejection_reason",
            field=models.TextField(blank=True, null=True),
        ),
    ]
