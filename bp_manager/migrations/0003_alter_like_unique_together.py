# Generated by Django 5.1.1 on 2024-09-18 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bp_manager", "0002_remove_blueprint_likes_like"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="like",
            unique_together={("user", "blueprint")},
        ),
    ]
