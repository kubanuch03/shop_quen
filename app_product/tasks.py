from celery import shared_task
from .models import Product


@shared_task
def bar():
    return 'Hello'