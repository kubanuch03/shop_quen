from django.db import models
from app_product.models import Product



class NewCollection(models.Model):
    product = models.ManyToManyField(Product,blank=True,null=True)
 
    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            
        ]



class Recommendations(models.Model):
    product = models.ManyToManyField(Product)

    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            
        ]

