# Generated by Django 4.1.7 on 2023-12-21 02:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_request", "0004_datarequest_date_completed_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscription",
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
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                (
                    "institution",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
        migrations.AddField(
            model_name="datarequest",
            name="subscriptions",
            field=models.ManyToManyField(to="data_request.subscription"),
        ),
    ]