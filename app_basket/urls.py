from django.urls import path
from .views import AddProductsBasketItem, ListBasketItem

urlpatterns = [
    path('add/products/basket/', AddProductsBasketItem.as_view(), name='add_multiple_products_to_basket'),
    path('list/basket/item/', ListBasketItem.as_view()),
]