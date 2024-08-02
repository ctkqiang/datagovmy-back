# Generated by Django 4.2.6 on 2024-02-06 01:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("community_product", "0005_communityproduct_problem_statement_en_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="communityproduct",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("ms", "Bahasa Melayu")],
                default="en",
                max_length=2,
            ),
        ),
    ]