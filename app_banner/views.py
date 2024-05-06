from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Banner

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializer import BannerCRUDserializer

class BannerCreate(generics.CreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCRUDserializer
    permission_classes = [IsAdminUser]


class BannerList(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCRUDserializer
    permission_classes = [AllowAny]


class BannerDetail(generics.RetrieveAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCRUDserializer
    permission_classes = [AllowAny]

class BannerDeleteandREtvew(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCRUDserializer
    permission_classes = [IsAdminUser]