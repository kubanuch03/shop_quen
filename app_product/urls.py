from django.urls import path
from app_product.views import ListAllProductApiView, CreateProductApiView, ProductRUBApiView

urlpatterns = [
    path('list/all/product/', ListAllProductApiView.as_view()),
    path('create/product/', CreateProductApiView.as_view()),
    path('rud/product/<int:id>', ProductRUBApiView.as_view()),
]