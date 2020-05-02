# from celery import shared_task
from celery.task import task

# @shared_task
@task
def fetch_url(url_id):
    if url_id is not None:
        print(f"Getting url for id: {url_id}")
    else:
        print("No url_id provided")
