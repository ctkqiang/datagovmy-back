# Generated by Django 4.1.7 on 2023-12-21 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("data_request", "0007_subscription_language"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="datarequest",
            name="email",
        ),
        migrations.RemoveField(
            model_name="datarequest",
            name="institution",
        ),
        migrations.RemoveField(
            model_name="datarequest",
            name="language",
        ),
        migrations.RemoveField(
            model_name="datarequest",
            name="name",
        ),
        migrations.RemoveField(
            model_name="datarequest",
            name="subscriptions",
        ),
        migrations.AddField(
            model_name="subscription",
            name="data_request",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="data_request.datarequest",
            ),
        ),
        migrations.AddConstraint(
            model_name="subscription",
            constraint=models.UniqueConstraint(
                fields=("email", "data_request"), name="unique_subscription"
            ),
        ),
    ]