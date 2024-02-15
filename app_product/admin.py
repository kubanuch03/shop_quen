from django.contrib import admin
from app_product.models import Product, Size, Color



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subcategory", "price", "brand", "description", "characteristics")


admin.site.register(Size)
admin.site.register(Color)