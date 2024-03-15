from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import json


from django_redis import cache as redis_cache
from django_redis import get_redis_connection

from app_product.models import Product
# from app_basket.serializer import BasketSerializer




class AddProductsBasketItem(APIView):
    def post(self, request):
        user = request.user
        basket_cache_key = f'basket_{user.id}'
        
        redis_connection = get_redis_connection("default")
        
        basket_data = redis_connection.get(basket_cache_key)
        
        if basket_data:
            basket_data = basket_data.decode('utf-8')
            basket_data = json.loads(basket_data)

            # basket_data_json = BasketSerializer(basket_data).data
            # basket_data = BasketSerializer(data=basket_data_json).data

        else:
            basket_data = {'items': []}

        products_data = request.data.get('products', [])
        # products_data = request.data.all()

        if not products_data:
            return Response("Запрос не содержит продуктов для добавления в корзину", status=status.HTTP_400_BAD_REQUEST)

        for product_data in products_data:
            product_id = product_data.get('product_id')

            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response(f"Продукт с id {product_id} не существует", status=status.HTTP_404_NOT_FOUND)


            quantity = product_data.get('quantity', 1)
            if quantity <= 0:
                return Response("Количество продукта должно быть положительным", status=status.HTTP_400_BAD_REQUEST)


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

        redis_connection.set(basket_cache_key, json.dumps(basket_data), ex=12345678)

        return Response("Продукты успешно добавлены в корзину", status=status.HTTP_201_CREATED)





class ListBasketItem(APIView):

    def get(self, request, format=None):
        user = request.user
        basket_cache_key = f'basket_{user.id}'

        redis_connection = get_redis_connection("default")
        basket_data = redis_connection.get(basket_cache_key)

        if basket_data:
            basket_data = basket_data.decode('utf-8')
            basket_data = json.loads(basket_data)
            return Response(basket_data, status=status.HTTP_200_OK)
        else:
            return Response({"Корзина пуста или отсутствует в кеше."}, status=status.HTTP_404_NOT_FOUND)


