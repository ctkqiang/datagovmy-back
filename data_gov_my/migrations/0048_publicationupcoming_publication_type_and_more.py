# Generated by Django 4.1.7 on 2023-08-18 03:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_gov_my", "0047_publicationupcoming_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="publicationupcoming",
            name="publication_type",
            field=models.CharField(default="cpi", max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="publicationupcoming",
            name="publication_type_title",
            field=models.CharField(default="cpi", max_length=100),
            preserve_default=False,
        ),
    ]