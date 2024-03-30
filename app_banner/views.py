from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Banner
from .serializer import BannerCRUDserializer

class BannerCreate(generics.CreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCRUDserializer
    permission_classes = [IsAdminUser]


class BannerList(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCRUDserializer
    permission_classes = [AllowAny]

class BannerDeleteandREtvew(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerCRUDserializer
    permission_classes = [IsAdminUser]