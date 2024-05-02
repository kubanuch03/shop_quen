# @shared_task
# def update_product_cache():
#     try:
#         queryset = Product.objects.all().select_related('subcategory').prefetch_related('characteristics', 'color', 'size').order_by('-id')
#         serializer = ProductListSerializer(queryset, many=True)
#         serialized_data = serializer.data

#         # Кешируем результаты на 10 секунд
#         cache.set('cached_products', serialized_data, timeout=10)
#         logger.info("Товары успешно закешированы")
#     except Exception as e:
#         logger.error(f"Ошибка кеширования товаров: {str(e)}")


# class ListAllProductApiView(ListAPIView): # Было 5 стало 5
#     queryset = Product.objects.all().select_related('subcategory').prefetch_related('characteristics', 'color', 'size').order_by('-id')
#     serializer_class = ProductListSerializer
#     filter_backends = [PriceRangeFilter, SearchFilter]
#     pagination_class = ListProductPagination


#     def get_queryset(self):
#         cached_data = cache.get('cached_products')
#         if cached_data:
#             logger.info("Using cached data")
#             # Просто возвращаем queryset, если данные закешированы
#             return super().get_queryset()  
#         else:
#             update_product_cache.delay()
#             logger.info("Started task to cache data")
#             # Возвращаем queryset, если данные не закешированы
#             return super().get_queryset()

#============================================================================================================