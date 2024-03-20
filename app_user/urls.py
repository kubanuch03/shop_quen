from django.urls import path
from .views import *


app_name = "users"
urlpatterns = [
    path("list/user/", UserListView.as_view(), name="list_user"),
    path("delete/user/<int:pk>/", UserDeleteView.as_view(), name="delete_user"),
    path("update/user/", UserUpdateView.as_view(), name="update_user"),
    path("register/user/", RegisterUserView.as_view(), name="register_user"),
    path("login/user/", LoginUserView.as_view(), name="login_user"),
    path("confirm-email/", ConfirmEmailView.as_view(), name="confirm_email"),
]
