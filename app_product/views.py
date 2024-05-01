from app_product.serializer import ProductDetailSerializer, ProductcreateSerializer, SizeSerializer, ColorSerializer, CharacteristikSerializer, ProductListSerializer,IsFavoriteDeleteSerializer
from app_product.models import Product, Size, Color, CharacteristikTopik, IsFavorite
from app_product.filters import PriceRangeFilter, SearchFilter
from app_favorite.models import Favorite

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
ListAPIView, CreateAPIView, UpdateAPIView, 
DestroyAPIView, ListCreateAPIView,
RetrieveUpdateDestroyAPIView, RetrieveAPIView
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, response

from app_product.permissions import IsCreatorOrAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import Http404


from .pagination import ListProductPagination



class ListAllProductApiView(ListAPIView): # Было 5 стало 5
    queryset = Product.objects.all().select_related('subcategory').prefetch_related('characteristics', 'color', 'size').order_by('-id')
    serializer_class = ProductListSerializer
    filter_backends = [PriceRangeFilter, SearchFilter]
    pagination_class = ListProductPagination

    @method_decorator(cache_page(15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


        



class CreateProductApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    permission_classes = [IsAdminUser, ]


        

        

 

class ProductDeleteApiView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    lookup_field = "id"
    permission_classes = [IsCreatorOrAdmin, ]



class ProductUpdateApiView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    lookup_field = "id"
    permission_classes = [IsAdminUser, ]

    
    def perform_update(self, serializer):
        instance = serializer.instance
        instance.price = serializer.apply_discount_to_price(instance.price, serializer.validated_data.get('discount', 0))
        instance.save()


class ListOneProducApiView(APIView):   
    serializer_class = ProductDetailSerializer

    def get(self, request, id):
        product = get_object_or_404(
            Product.objects.select_related('subcategory')
            .prefetch_related('characteristics', 'color', 'size'),id=id
        )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)
    

class ProductBySubCategory(APIView):  #Было 7 SQL запроса стало 4
    serializer_class = ProductDetailSerializer
    
    def get(self, request, subcategory_id):
        products = Product.objects.filter(subcategory_id=subcategory_id)\
            .select_related('subcategory')\
            .prefetch_related('characteristics', 'color', 'size')
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)


class ProductAllDeleteAllApiView(APIView):
    serializer_class = None
    def delete(self, request, *args, **kwargs):
        try:
            Product.objects.all().delete()
            return Response({'detail': 'All objects deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'detail': 'Failed to delete all objects'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#=== Size ================================================================================================================================================



class SizeListApiView(ListAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [AllowAny]

    @method_decorator(cache_page(13))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SizeDetailApiView(RetrieveAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [AllowAny]


class SizeCreateApiView(CreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser, ]



class SizeRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser, ]
    lookup_field = "id"




#=== Color ================================================================================================================================================


class ColorListApiView(ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [AllowAny, ]

    # @method_decorator(cache_page(10))
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

class ColorDeatilApiView(RetrieveAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [AllowAny, ]


class ColorCreateApiView(CreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser, ]
    
  
    

class ColorRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser, ]
    lookup_field = "id"


#==== Characteristik ============================

class CharacteristikViewSet(ModelViewSet):
    queryset = CharacteristikTopik.objects.all()
    serializer_class = CharacteristikSerializer
    permission_classes = [IsAdminUser]

   
    

class CharacteristikListView(ListAPIView):
    queryset = CharacteristikTopik.objects.all()
    serializer_class = CharacteristikSerializer

    @method_decorator(cache_page(10))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
  

class CharacteristikDetailView(RetrieveAPIView):
    queryset = CharacteristikTopik.objects.all()
    serializer_class = CharacteristikSerializer

    # def get(self, request, id):
    #     products = get_object_or_404(Product, id=id)
    #     serializer = CharacteristikSerializer(products)
    #     return Response(serializer.data)
    



class IsFavoriteApiView(DestroyAPIView):
    queryset = IsFavorite.objects.all()
    serializer_class = IsFavoriteDeleteSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            # Ищем объект IsFavorite по полю product
            obj = IsFavorite.objects.get(product=self.kwargs['product'])
            # Проверяем, принадлежит ли объект текущему пользователю
            if obj.user != self.request.user:
                raise Http404("You cannot delete this favorite object.")
            return obj
        except IsFavorite.DoesNotExist:
            raise Http404("Favorite object does not exist.")

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Удаление связанных объектов из модели Favorite
            instance.favorite.delete()
            # Удаление объекта из модели IsFavorite
            self.perform_destroy(instance)
            return Response({"success": "Deleted!"}, status=status.HTTP_204_NO_CONTENT)
        except Http404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)