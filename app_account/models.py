from django.db import models
from django.db import models
from app_user.models import CustomUser 
from app_product.models import Product, Size, Color


class PaymentMethod(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return self.text
    


class Deliver(models.Model):
    types = models.CharField(max_length=255)
    location = models.CharField(max_length=255)


# class Author(models.Model):
#     lastname = models.CharField(max_length=255)
#     firstname = models.CharField(max_length=255)


class History(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    price = models.PositiveIntegerField()
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    # location = models.CharField(max_length=255)
    deliver = models.ForeignKey(Deliver, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=255)