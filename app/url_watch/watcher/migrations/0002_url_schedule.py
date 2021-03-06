# Generated by Django 2.2.12 on 2020-05-01 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0012_periodictask_expire_seconds'),
        ('watcher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='schedule',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='url_interval_schedule', to='django_celery_beat.IntervalSchedule'),
            preserve_default=False,
        ),
    ]
