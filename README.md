# url_watch

## A quick n dirty url watcher

This program leverages Django, Postgres, Celery, RabbitMQ, django_celery_beat and Docker

### Usage

#### Dependencies

* Docker
* docker-compose

#### Installation

Install Docker and docker-compose

run `docker compose up` from this directory

`docker-compose` will build and start all containers

Once the containers are all ready, open your web browser and point it at:

http://127.0.0.1:8000/watcher/

There are 2 screens: the `Add Url` screen and the `URL List` screen where one can drill down into the data collected by Celery, et al.

### Note & Warning

All Django & DRF endpoint Authentication is set to allow any user to submit urls and monitor the ones submitted. Do not use this software for anything public-facing.