from django.db import models

class PaymentMethod(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return self.text