from django.db import models

class Banner(models.Model):
    topik_baner = models.ManyToManyField('TopikBaner')

    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            
        ]

class TopikBaner(models.Model):
    name = models.CharField(max_length=250)
    images = models.ImageField(upload_to='banner/')
    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            
        ]