from django.urls import path
from rest_framework.routers import DefaultRouter

from app_product.views import *
router = DefaultRouter()
router.register(r"characteristik",CharacteristikViewSet, basename='characteristik')

urlpatterns = [
    path('list/all/product/', ListAllProductApiView.as_view(), name='list-all-product'),
    path('list/all/product/', ListAllAdminProductApiView.as_view(), name='list-all-admin-product'),
    path('list/one/product/<int:id>/', ListOneProducApiView.as_view(), name='list-one-product'),
    path('create/product/', CreateProductApiView.as_view(),name='create-product',),
    path('update/product/<int:id>/', ProductUpdateApiView.as_view(),name='update-product'),
    path('delete/product/<int:id>/', ProductDeleteApiView.as_view(),name='delete-product-id'),
    path('subcategories/<int:subcategory_id>/products/', ProductBySubCategory.as_view(),name='subcategory-id-products'),
    path('delete/all/product/', ProductAllDeleteAllApiView.as_view(),name='delete-all-product'),


    path('list/sizes/', SizeListApiView.as_view(),name='list-sizes'),
    path('detail/sizes/<int:pk>/', SizeListApiView.as_view(),name='detail-sizes'),
    path('create/sizes/', SizeCreateApiView.as_view(),name='create-sizes'),
    path('rud/sizes/<int:id>/', SizeRUDView.as_view(),name='rud-sizes-id'),

    path('list/colors/', ColorListApiView.as_view(),name='list-color'),
    path('detail/colors/<int:pk>/', ColorDeatilApiView.as_view(),name='detail-color-id'),
    path('create/colors/', ColorCreateApiView.as_view(),name='create-color'),
    path('rud/colors/<int:id>/', ColorRUDView.as_view(),name='rud-color-id'),

    path('list/characteristik/', CharacteristikListView.as_view(),name='list-characteristik'),
    path('detail/characteristik/<int:pk>/', CharacteristikDetailView.as_view(),name='detail-characteristik-id'),

    path('delete/isfavorite/<int:product>/', IsFavoriteApiView.as_view(),name='delete-is_favorite'),


]+ router.urls