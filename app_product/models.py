from django.db import models
from app_category.models import SubCategory
from app_user.models import  CustomUser
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

class Color(models.Model):
    colors = models.CharField(max_length=255)

    def __str__(self):
        return self.colors
    
    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            models.Index(fields=['colors']),  
            
        ]

class Size(models.Model):
    sizes = models.CharField(max_length=255)

    def __str__(self):
        return self.sizes
    
    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            models.Index(fields=['sizes']),  
            
        ]


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    brand = models.CharField(max_length=255)
    characteristics = models.ManyToManyField('CharacteristikTopik')
    is_any = models.BooleanField(default=False)
    color = models.ManyToManyField(Color)
    size = models.ManyToManyField(Size)
    discount = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)
    images1 = models.ImageField(upload_to="text/", blank=True, null=True)
    images2 = models.ImageField(upload_to="text/", blank=True, null=True)
    images3 = models.ImageField(upload_to="text/", blank=True, null=True)


    class Meta:
        indexes = [
            models.Index(fields=['id']), 
            models.Index(fields=['title']), 
            models.Index(fields=['brand']),  
        ]

class CharacteristikTopik(models.Model):
    title = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    indexes = [
            models.Index(fields=['id']),  
            models.Index(fields=['title']),  
            models.Index(fields=['value']),  
            
        ]


