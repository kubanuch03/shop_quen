from django.urls import path
from .views import BannerList, BannerDeleteandREtvew,BannerCreate, BannerDetail

urlpatterns = [
    path('banners/', BannerList.as_view(), name='banner-list'),
    path('banners/create/', BannerCreate.as_view(), name='banner-create'),
    path('banners/delete/<int:pk>/', BannerDeleteandREtvew.as_view(), name='banner-delete'),
    path('banners/detail/<int:pk>/', BannerDetail.as_view(), name='banner-detail'),
]