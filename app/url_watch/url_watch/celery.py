import os
import hashlib
import requests
import difflib

from celery import Celery
from celery.task import task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_watch.settings')

import django
django.setup()

from watcher.models import Url, UrlWatchResult

app = Celery('url_watch', broker="pyamqp://user:passwd@rabbitmq")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


class NoUrlProvided(Exception):
    pass


@task
def fetch_url(url, creator_uuid):
    if url is None:
        raise NoUrlProvided()

    url_obj = Url.objects.filter(
        creator_uuid=creator_uuid,
        url=url
    ).first()

    if url_obj is None:
        raise Url.DoesNotExist

    response = requests.get(url)

    if response.status_code == requests.codes.ok:

        sha2 = hashlib.sha256(f"{response.text}".encode('utf-8')).hexdigest();

        previous = UrlWatchResult.objects.only(
            'content_hash'
        ).filter(
            creator_uuid=creator_uuid,
            url=url_obj,
        ).order_by(
            '-id'
        ).first()

        content = response.text
        diff = None
        if previous is not None:
            if previous.content_hash == sha2:
                content = None
            else:
                previous_result = UrlWatchResult.objects.filter(
                    url=url_obj
                ).exclude(
                    content_hash=sha2
                ).order_by('-id').first()

                if previous_result is not None:
                    # diff these 2...
                    content_new = content.strip().splitlines()
                    content_old = previous_result.content.strip().splitlines()

                    result = difflib.unified_diff(
                        content_new,
                        content_old,
                        fromfile=previous.content_hash,
                        tofile=sha2,
                        lineterm=''
                    )
                    diff = "\n".join(result)

        UrlWatchResult.objects.create(
            creator_uuid=creator_uuid,
            url=url_obj,
            content_hash=sha2,
            content=content,
            status=response.status_code,
            diff=diff
        )
    else:
        # not a 200
        UrlWatchResult.objects.create(
            creator_uuid=creator_uuid,
            url=url_obj,
            content_hash=None,
            content=None,
            error=response.status_code
        )
