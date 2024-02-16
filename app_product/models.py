from django.db import models
from app_category.models import SubCategory


class Color(models.Model):
    colors = models.CharField(max_length=255)

    def __str__(self):
        return self.colors
    

class Size(models.Model):
    sizes = models.CharField(max_length=255)

    def __str__(self):
        return self.sizes


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    brand = models.CharField(max_length=255)
    characteristics = models.TextField()
    is_any = models.BooleanField(default=False)
    color = models.ManyToManyField(Color)
    size = models.ManyToManyField(Size)


    images1 = models.ImageField(upload_to="app_product/image/", blank=True, null=True)
    images2 = models.ImageField(upload_to="app_product/image/", blank=True, null=True)
    images3 = models.ImageField(upload_to="app_product/image/", blank=True, null=True)

