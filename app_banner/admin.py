from django.contrib import admin
from .models import Banner, TopikBaner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id',)  

@admin.register(TopikBaner)
class BannerTopikAdmin(admin.ModelAdmin):
    list_display = ('id','name','images',) 