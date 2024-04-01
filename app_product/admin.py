from django.contrib import admin
from .models import Product, Size, Color, CharacteristikTopik



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subcategory", "price", "brand", "description")



class ColorAdmin(admin.ModelAdmin):
    list_display = ['id','colors']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['id','sizes']

class CharacteristikTopikAdmin(admin.ModelAdmin):
    list_display = ['id','title','value']

admin.site.register(Size,SizeAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(CharacteristikTopik,CharacteristikTopikAdmin)