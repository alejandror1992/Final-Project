# Generated by Django 4.2.1 on 2023-08-08 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppDjango', '0006_remove_medal_style_remove_style_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='styles',
        ),
    ]
