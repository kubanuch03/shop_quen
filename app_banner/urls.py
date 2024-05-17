from django.urls import path
from .views import *

urlpatterns = [
    path('banners/', BannerList.as_view(), name='banner-list'),
    path('banners/create/', BannerCreate.as_view(), name='banner-create'),
    path('banners/delete/<int:pk>/', BannerDeleteandREtvew.as_view(), name='banner-delete'),
    path('banners/detail/<int:pk>/', BannerDetail.as_view(), name='banner-detail'),

    path('topik/banners/', TopikBannerList.as_view(), name='topik/banner-list'),
    path('topik/banners/create/', TopikBannerCreate.as_view(), name='topik/banner-create'),
    path('topik/banners/delete/<int:pk>/', TopikBannerDeleteandREtvew.as_view(), name='topik/banner-delete'),
    path('topik/banners/detail/<int:pk>/', TopikBannerDetail.as_view(), name='topik/banner-detail'),
]
