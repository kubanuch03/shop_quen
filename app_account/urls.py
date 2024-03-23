from django.urls import path,include
from app_account.views import UserInfoApiView, LogoutView, PaymentMethodApiView, OrderHistory, SendResetAPiView, ChangePasswordAPIVIew



urlpatterns = [
    path('user/info/', UserInfoApiView.as_view()),
    path('logout/user/', LogoutView.as_view(), name='user logout'),
    path('payment/method/', PaymentMethodApiView.as_view()),
    path('order/history/', OrderHistory.as_view()),


    path('send/reset/code/', SendResetAPiView.as_view()),
    path('change/password/', ChangePasswordAPIVIew.as_view()),


]