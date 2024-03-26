from django.urls import path
from .views import *


app_name = "users"
urlpatterns = [
    path("list/user/", UserListView.as_view(), name="list_user"),
    path("detail/user/", UserDetailView.as_view(), name="detail_user"),
    path("delete/user/<int:pk>/", UserDeleteView.as_view(), name="delete_user"),
    path("update/user/<int:pk>/", UserUpdateView.as_view(), name="update_user"),

    path("register/user/", RegisterUserView.as_view(), name="register_user"),
    path("login/user/", LoginUserView.as_view(), name="login_user"),

    path('send-code-to-email/', ForgetPasswordSendCodeView.as_view(), name='send_password_reset_code'), # отправить code в почту
    path('forget-password/reset/',ForgetPasswordView, name='reset_password'), # забыл пароль при входе
    path('verify/register-code/', VerifyUserCodeView.as_view(), name='verify_user_code'),
]
