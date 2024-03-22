from rest_framework.generics import ListAPIView
from app_user.models import CustomUser
from app_account.serializer import (
    UserInfoSerializer,
    PaymentMethodSerializer)
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status

from app_account.models import PaymentMethod
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection

import json




class PaymentMethodApiView(generics.ListCreateAPIView):
    queryset = PaymentMethod.objects.values('text')
    serializer_class = PaymentMethodSerializer



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
        

class OrderHistory(APIView):

    def get(self, request, format=None):
        user = request.user
        basket_cache_key = f'basket_{user.id}'

        redis_connection = get_redis_connection("default")
        basket_data = redis_connection.get(basket_cache_key)

        if basket_data:
            basket_data = basket_data.decode('utf-8')
            basket_data = json.loads(basket_data)
            return Response(basket_data, status=status.HTTP_200_OK)
        else:
            return Response({"Корзина пуста или отсутствует в кеше."}, status=status.HTTP_404_NOT_FOUND)