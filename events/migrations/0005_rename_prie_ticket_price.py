# Generated by Django 5.0.9 on 2024-11-09 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_rename_user_ticket_owner"),
    ]

    operations = [
        migrations.RenameField(model_name="ticket", old_name="prie", new_name="price",),
    ]
