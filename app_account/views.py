from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateAPIView
from app_user.models import CustomUser
from app_account.serializer import (
    UserInfoSerializer,
    PaymentMethodSerializer,
    SendResetCodeSerializer,
    ChangePasswordSerializer,
    HistoryCreateSerializer,
    HistoryListSerializer,
    ChangeUserInfoSerializer,)
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from app_account.utils import send_verification_mail

from rest_framework import permissions
from django.utils.crypto import constant_time_compare
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from app_account.models import History

from django.utils import timezone
from app_account.models import PaymentMethod
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status





class PaymentMethodApiView(generics.ListCreateAPIView):
    queryset = PaymentMethod.objects.values('text')
    serializer_class = PaymentMethodSerializer



class UserInfoApiView(ListAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(id=user.id)
    


class UserUpdateApiView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all() 
    serializer_class = ChangeUserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    


class ChangeUserInfoApiView(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(id=user.id)
    


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Error logging out.'}, status=status.HTTP_400_BAD_REQUEST)


class SendResetAPiView(UpdateModelMixin, GenericAPIView):
    serializer_class = SendResetCodeSerializer

    def get_object(self):
        user = CustomUser.objects.get(email=self.request.data.get('email'))
        return user

    def patch(self, *args, **kwargs):
        try:
            email = self.get_object().email
        except ObjectDoesNotExist:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        send_verification_mail(email)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)




class ChangePasswordAPIVIew(UpdateModelMixin, GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = CustomUser.objects.get(id=self.request.user.id)
        return user

    def patch(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            new_password = self.request.data.get('new_password')
            confirming_new_password = self.request.data.get('confirming_new_password')
            if constant_time_compare(new_password, confirming_new_password):
                user = self.get_object()
                user.password = make_password(confirming_new_password)
                user.save()
                return Response({'Вы ушпешно поменяли свой пароль'}, status=status.HTTP_200_OK)
            else:
                return Response({'Пароли не совподают'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)



class HistoryListApiView(ListAPIView):
    queryset = History.objects.all()
    serializer_class = HistoryListSerializer



class HistoryCreateApiView(CreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistoryCreateSerializer





class HistoryDetailView(generics.RetrieveUpdateAPIView):
    queryset = History.objects.all()
    serializer_class = HistoryCreateSerializer
    lookup_field = "id"


