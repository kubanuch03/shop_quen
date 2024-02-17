from django.urls import path
from app_product.views import ListAllProductApiView, CreateProductApiView, ProductDeleteApiView, ProductUpdateApiView, ListOneProducApiView, ProductBySubCategory

urlpatterns = [
    path('list/all/product/', ListAllProductApiView.as_view()),
    path('list/one/product/<int:id>/', ListOneProducApiView.as_view()),
    path('create/product/', CreateProductApiView.as_view()),
    path('update/product/<int:id>', ProductUpdateApiView.as_view()),
    path('delete/product/<int:id>', ProductDeleteApiView.as_view()),
    path('subcategories/<int:subcategory_id>/products/', ProductBySubCategory.as_view()),
]