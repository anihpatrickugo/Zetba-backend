# Generated by Django 5.0.9 on 2024-11-26 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_notifications_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="notifications",
            name="read",
            field=models.BooleanField(default=False),
        ),
    ]
