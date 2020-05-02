# Generated by Django 2.2.12 on 2020-05-01 14:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0002_url_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='schedule',
        ),
        migrations.AddField(
            model_name='url',
            name='every',
            field=models.IntegerField(default=1, help_text='Number of interval periods to wait before checking the URL again', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Every'),
        ),
        migrations.AddField(
            model_name='url',
            name='period',
            field=models.CharField(choices=[('days', 'Days'), ('hours', 'Hours'), ('minutes', 'Minutes'), ('seconds', 'Seconds')], default='minutes', help_text='The type of period between URL checks (Example: days)', max_length=24, verbose_name='Interval'),
        ),
    ]