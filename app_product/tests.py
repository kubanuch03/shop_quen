# @shared_task
# def update_product_cache():
#     queryset = Product.objects.all().select_related('subcategory').prefetch_related('characteristics', 'color', 'size').order_by('-id')[:50]
#     serialized_data = [product.pk for product in queryset]
#     cache.set('product_cache', serialized_data, timeout=5)


# class ListAllProductApiView(ListAPIView): # Было 5 стало 5
#     queryset = Product.objects.all().select_related('subcategory').prefetch_related('characteristics', 'color', 'size').order_by('-id')
#     serializer_class = ProductListSerializer
#     filter_backends = [PriceRangeFilter, SearchFilter]
#     pagination_class = ListProductPagination


#     def get_queryset(self):
#         self.update_product_cache_async()

#         cached_data = cache.get('product_cache')
#         if cached_data:
#             return Product.objects.filter(pk__in=cached_data)
#         else:
#             return self.get_initial_queryset_from_db()[:50]

#     def update_product_cache_async(self):
#         update_product_cache.apply_async()

#     def get_initial_queryset_from_db(self):
#         return Product.objects.all().select_related('subcategory').prefetch_related('characteristics', 'color', 'size').order_by('-id')

#============================================================================================================