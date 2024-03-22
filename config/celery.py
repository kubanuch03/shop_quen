from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from celery import Celery
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("config.celeryconfig")

app.conf.update(
    result_expires=3600,
)

app.autodiscover_tasks()
