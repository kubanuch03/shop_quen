from django.urls import path
from .views import *

urlpatterns = [
    path('banners/', BannerList.as_view(), name='banner-list'),
    path('banners/create/', BannerCreate.as_view(), name='banner-create'),
    path('banners/rud/<int:pk>/', BannerDeleteandREtvew.as_view(), name='banner-rud'),
    path('banners/detail/<int:pk>/', BannerDetail.as_view(), name='banner-detail'),

    path('topik/banners/', TopikBannerList.as_view(), name='topik/banner-list'),
    path('topik/banners/create/', TopikBannerCreate.as_view(), name='topik/banner-create'),
    path('topik/banners/rud/<int:pk>/', TopikBannerDeleteandREtvew.as_view(), name='topik/banner-rud'),
    path('topik/banners/detail/<int:pk>/', TopikBannerDetail.as_view(), name='topik/banner-detail'),
]
