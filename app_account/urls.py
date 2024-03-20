from django.urls import path,include
from app_account.views import UserInfoApiView, LogoutView, PaymentMethodApiView



urlpatterns = [
    path('user/info/', UserInfoApiView.as_view()),
    path('logout/user/', LogoutView.as_view(), name='user logout'),
    path('payment/method/', PaymentMethodApiView.as_view()),
]