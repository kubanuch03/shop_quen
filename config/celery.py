from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery import shared_task
from django.core.cache import cache
from datetime import timedelta
from celery.schedules import crontab

from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')


app.config_from_object('django.conf:settings', namespace='CELERY')




# В файле tasks.py

app.conf.beat_schedule = {
    'clear_cache_every_10_minutes': {
        'task': 'app_product.tasks.clear_cache',
        'schedule': timedelta(minutes=10),
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: ,{self.request!r}')
