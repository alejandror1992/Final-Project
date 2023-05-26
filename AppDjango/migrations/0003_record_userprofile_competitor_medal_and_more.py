# Generated by Django 4.2.1 on 2023-05-23 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppDjango', '0002_academy_featured_event_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('no_contest', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='competitor',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Medal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medal', models.CharField(choices=[('gold', 'Gold'), ('silver', 'Silver'), ('bronze', 'Bronze')], max_length=6)),
                ('count', models.IntegerField(default=0)),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medals', to='AppDjango.style')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='amateur_record',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amateur_profile', to='AppDjango.record'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='medals',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppDjango.medal'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='professional_record',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='professional_profile', to='AppDjango.record'),
        ),
    ]