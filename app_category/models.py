from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="app_category/Category_images/")

    def __str__(self) -> str:
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="app_category/SubCategory_images")
    creted_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


    
    