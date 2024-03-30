from django.contrib import admin
from .models import Product, Size, Color, CharacteristikTopik



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subcategory", "price", "brand", "description")


admin.site.register(Size)
admin.site.register(Color)
admin.site.register(CharacteristikTopik)