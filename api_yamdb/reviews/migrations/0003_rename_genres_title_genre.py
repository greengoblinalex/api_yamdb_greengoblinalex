# Generated by Django 3.2 on 2023-04-29 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='genres',
            new_name='genre',
        ),
    ]