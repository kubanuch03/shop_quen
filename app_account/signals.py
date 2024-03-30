from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import History

@receiver(post_save, sender=History)
def update_delivery_date(sender, instance, created, **kwargs):
    if instance.status == 'Доставлено':
        instance.delivery_date = timezone.now()
        instance.save()
