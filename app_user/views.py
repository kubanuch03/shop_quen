from django.core.cache import cache


from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate
from django.utils import timezone
from datetime import timedelta

from .models import CustomUser
from .serializers import UserSerializer, LoginUserSerializer, ConfirmEmailSerializer

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

    # def get(self, request, token):
    #     try:
    #         user = CustomUser.objects.get(activation_token=token)
    #         user.is_active = True
    #         user.save()
    #     except CustomUser.DoesNotExist:
    #         raise ({"error": "invalid-token"})
        




class ConfirmEmailView(generics.GenericAPIView):
    serializer_class = ConfirmEmailSerializer

    @staticmethod
    def get(request, token):
        try:
            user = CustomUser.objects.get(token_auth=token)
            if user.is_active:
                return Response(
                    {"detail": "User is already activated"}, status=status.HTTP_200_OK
                )

            user.is_active = True
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "detail": "Email confirmation successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Invalid token"}, status=status.HTTP_404_NOT_FOUND
            )


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        print("Before perform_create")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()

        print("After perform_create")
        return Response(
            {
                "detail": "Registration successful",
                "user_id": client.id,
                "email": client.email,
                "username": client.username,
            },
            status=status.HTTP_201_CREATED,
        )


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