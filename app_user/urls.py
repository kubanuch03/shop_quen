from django.urls import path
from .views import *


app_name = "users"
urlpatterns = [
    path("list/user/", UserListView.as_view(), name="list_user"),
    path("delete/user/<int:pk>/", UserDeleteView.as_view(), name="delete_user"),
    path("update/user/<int:pk>/", UserUpdateView.as_view(), name="update_user"),

    path("register/user/", RegisterUserView.as_view(), name="register_user"),
    path("login/user/", LoginUserView.as_view(), name="login_user"),

    path('verify/', VerifyUserCodeView.as_view(), name='verify_user_code'),
]
