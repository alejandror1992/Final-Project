# Generated by Django 4.2.1 on 2023-06-21 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppDjango', '0005_rename_siler_medal_silver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medal',
            name='style',
        ),
        migrations.RemoveField(
            model_name='style',
            name='name',
        ),
    ]