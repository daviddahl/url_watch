# Generated by Django 2.2.12 on 2020-05-01 18:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0003_auto_20200501_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='url',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='UrlWatchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator_uuid', models.UUIDField()),
                ('content_hash', models.CharField(blank=True, max_length=64, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='url_url_watch_result', to='watcher.Url')),
            ],
        ),
    ]
