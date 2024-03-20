from django.shortcuts import render
from rest_framework.generics import ListAPIView
from app_user.models import CustomUser
from app_account.serializer import UserInfoSerializer, PaymentMethod
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from app_account.models import PaymentMethod


class PaymentMethodApiView(generics.ListCreateAPIView):
    queryset = PaymentMethod.objects.values('text')
    serializer_class = PaymentMethod



class UserInfoApiView(ListAPIView):
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