from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Banner, TopikBaner

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializer import BannerCRUDserializer, TopikBannerCRUDserializer

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





class TopikBannerCreate(generics.CreateAPIView):
    queryset = TopikBaner.objects.all()
    serializer_class = TopikBannerCRUDserializer
    permission_classes = [IsAdminUser]


class TopikBannerList(generics.ListAPIView):
    queryset = TopikBaner.objects.all()
    serializer_class = TopikBannerCRUDserializer
    permission_classes = [AllowAny]


class TopikBannerDetail(generics.RetrieveAPIView):
    queryset = TopikBaner.objects.all()
    serializer_class = TopikBannerCRUDserializer
    permission_classes = [AllowAny]

class TopikBannerDeleteandREtvew(generics.RetrieveUpdateDestroyAPIView):
    queryset = TopikBaner.objects.all()
    serializer_class = TopikBannerCRUDserializer
    permission_classes = [IsAdminUser]