from django.contrib import admin
from app_user.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email','username','id']

admin.site.register(CustomUser,CustomUserAdmin)