from django.urls import path,include
from app_account.views import UserInfoApiView, LogoutView, PaymentMethodApiView, OrderHistory



urlpatterns = [
    path('user/info/', UserInfoApiView.as_view()),
    path('logout/user/', LogoutView.as_view(), name='user logout'),
    path('payment/method/', PaymentMethodApiView.as_view()),
    path('order/history/', OrderHistory.as_view()),

]