from django.db import models
from django.db import models
from app_user.models import CustomUser 
from app_product.models import Product, Size, Color
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



class PaymentMethod(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return self.text
    
    
    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            
        ]
        ordering = ['-id']




class History(models.Model):
    STATUS = (
        ('На проверке', 'На проверке'),
        ('Оплачено', 'Оплачено'),
        ('Доставлено', 'Доставлено'),

    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField('ProductInstance',related_name='histories')
    price = models.PositiveIntegerField()
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    types = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS, default='На проверке')
    delivery_date = models.DateTimeField(null=True, blank=True)

    @staticmethod
    @receiver(post_save, sender='app_account.History')
    def update_delivery_date(sender, instance, **kwargs):
        if instance.status == 'Доставлено' and not instance.delivery_date:
            instance.delivery_date = timezone.now()
            instance.save()


    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            
        ]


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    history = models.ForeignKey(History, on_delete=models.CASCADE,related_name='product_instances')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

