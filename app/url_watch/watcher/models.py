from uuid import uuid4
import hashlib

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django_celery_beat.models import PeriodicTask, IntervalSchedule

DAYS = 'days'
HOURS = 'hours'
MINUTES = 'minutes'
SECONDS = 'seconds'

PERIOD_CHOICES = (
    (DAYS, 'Days'),
    (HOURS, 'Hours'),
    (MINUTES, 'Minutes'),
    (SECONDS, 'Seconds'),
)

# PeriodicTask:
# name, task, IntervalSchedule FK, start_time (timezone.now()), args = "["the url"]"
TASK_NAME = "url_watch.celery.fetch_url"


class Url(models.Model):
    """
    The Url and interval
    """
    creator_uuid = models.UUIDField(primary_key=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField()
    every = models.IntegerField(
        null=False,
        verbose_name='Every',
        help_text='Number of interval periods to wait before '
                    'checking the URL again',
        validators=[MinValueValidator(1)],
        default=1
    )
    period = models.CharField(
        max_length=24,
        choices=PERIOD_CHOICES,
        verbose_name='Interval',
        help_text='The type of period between URL checks (Example: days)',
        default=MINUTES
    )

    def save(self, *args, **kwargs):
        if getattr(self, 'id') is None:
            # this is a new Url, lets create the PeriodicTask
            interval_schedule, created = IntervalSchedule.objects.get_or_create(
                every=self.every,
                period=self.period
            )
            PeriodicTask.objects.create(
                name=f"{self.creator_uuid}|{uuid4()}", # unique name
                task=TASK_NAME,
                interval=interval_schedule,
                start_time=timezone.now(),
                args=f'["{self.url}", "{self.creator_uuid}"]'
            )

        super(Url, self).save(*args, **kwargs)


class UrlWatchResult(models.Model):
    """
    The results of a Url watcher task
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator_uuid = models.UUIDField(primary_key=False)
    url = models.ForeignKey(
        Url,
        related_name='url_url_watch_result',
        on_delete=models.CASCADE
    )
    content_hash = models.CharField(max_length=64, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=0) # 0 is unknown perhaps
    diff = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.url.url}: {self.content_hash}: {self.status}"
