from django.contrib import admin
from app_account.models import PaymentMethod, History, Deliver


admin.site.register(PaymentMethod)
admin.site.register(History)
admin.site.register(Deliver)