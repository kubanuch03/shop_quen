from django.core.cache import cache

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate
from django.utils import timezone
from datetime import timedelta

from .models import CustomUser
from .serializers import UserSerializer, LoginUserSerializer, ConfirmEmailSerializer, VerifyUserCodeSerializer

import time


class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if email and password:
            
            user = authenticate(username=email, password=password)

            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "user_id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "detail": "Authentication failed. User not found or credentials are incorrect."
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"detail": "Invalid input. Both email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )







class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class VerifyUserCodeView(generics.GenericAPIView):
    serializer_class = VerifyUserCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = request.data.get("code")
        if not code:
            return Response({"code": ["Это поле обязательно."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(code=code)
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user=user)
            return Response({
                "message": "Учетная запись успешно активирована.",
                'id':user.id,
                'email':user.email,
                'refresh-token': str(refresh),
                'access': str(refresh.access_token),
                'refresh_lifetime_days': refresh.lifetime.days,
                'access_lifetime_days': refresh.access_token.lifetime.days

                })
        except CustomUser.DoesNotExist:
            return Response({"message": "Неверный код подтверждения."}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]