# Generated by Django 5.0.3 on 2024-03-23 08:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("minor_app", "0004_message_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="category",
            field=models.IntegerField(
                choices=[(1, "Concept"), (2, "Music")], default=1
            ),
        ),
    ]
