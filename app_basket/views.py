from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Basket, BasketItem
from .serializer import BasketItemSerializer
from app_product.models import Product
from django.core.cache import cache
from rest_framework.views import APIView



class AddProductsBasketItem(APIView):
    def post(self, request, format=None):
        user = request.user
        basket_cache_key = f'basket_{user.id}'
        basket_data = cache.get(basket_cache_key) or {'items': []}

        products_data = request.data.get('products', [])

        for product_data in products_data:
            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity', 1)

            product = Product.objects.get(pk=product_id)
            product_price = product.price * quantity

            product_info = {
                'product_id': product_id,
                'title': product.title,
                'price': product.price,
                'quantity': quantity,
                'total': product_price
            }

            basket_data['items'].append(product_info)

        total_price = sum(item['total'] for item in basket_data['items'])
        basket_data['total'] = total_price

        cache.set(basket_cache_key, basket_data, timeout=12345677)

        return Response("Продукты успешно добавлены в корзину", status=status.HTTP_201_CREATED)





class ListBasketItem(APIView):

    def get(self, request, format=None):
        user = request.user
        basket_cache_key = f'basket_{user.id}'
        basket_data = cache.get(basket_cache_key)

        if basket_data:
            return Response(basket_data, status=status.HTTP_200_OK)
        else:
            return Response({"Корзина пуста или отсутствует в кеше."}, status=status.HTTP_404_NOT_FOUND)


