from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255,blank=True,null=True,)
    created_at = models.DateField(auto_now_add=True,blank=True,null=True,)
    image = models.ImageField(upload_to="app_category/",blank=True,null=True,)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['title']), 
            models.Index(fields=['id']),  
        ]



class SubCategory(models.Model):
    # category = models.ForeignKey(Category, blank=True,null=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="text/")
    creted_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['title']), 
            models.Index(fields=['id']),  
        ]



    
    