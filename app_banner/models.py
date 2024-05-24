from django.db import models

class Banner(models.Model):
    topik_baner = models.ManyToManyField('TopikBaner')

    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            
        ]
        ordering = ['id'] 

class TopikBaner(models.Model):
    name = models.CharField(max_length=250,blank=True,null=True)
    images = models.ImageField(upload_to='banner/',blank=True,null=True)
    class Meta:
        indexes = [
            models.Index(fields=['id']),  
            
        ]