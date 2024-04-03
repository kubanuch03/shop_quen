from app_product.serializer import ProductListSerializer, ProductcreateSerializer, SizeSerializer, ColorSerializer, CharacteristikSerializer
from app_product.models import Product, Size, Color, CharacteristikTopik
from app_product.filters import PriceRangeFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
ListAPIView, CreateAPIView, UpdateAPIView, 
DestroyAPIView, ListCreateAPIView,
RetrieveUpdateDestroyAPIView, RetrieveAPIView
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from app_product.permissions import IsCreatorOrAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.cache import cache_page


class ListAllProductApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [PriceRangeFilter, SearchFilter]
    permission_classes = [AllowAny, ]
    pagination_class = PageNumberPagination

    @method_decorator(cache_page(60*60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CreateProductApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    permission_classes = [IsAuthenticated, ]




class ProductDeleteApiView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    lookup_field = "id"
    permission_classes = [IsCreatorOrAdmin, ]



class ProductUpdateApiView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated, ]


    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(id=self.kwargs[self.lookup_field]).first()
        if obj is None:
            raise Http404("Product does not exist")
        return obj
    
    def perform_update(self, serializer):
        instance = serializer.instance
        instance.price = serializer.apply_discount_to_price(instance.price, serializer.validated_data.get('discount', 0))
        instance.save()


class ListOneProducApiView(APIView):
    permission_classes = [AllowAny,]

    @method_decorator(cache_page(60*60)) 
    def get(self, request, id):
        products = get_object_or_404(Product, id=id)
        serializer = ProductListSerializer(products)
        return Response(serializer.data)
    

class ProductBySubCategory(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, subcategory_id):
        products = get_object_or_404(Product,subcategory_id=subcategory_id)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    



class SizeApiView(ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser, ]


class SizeRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser, ]
    lookup_field = "id"


class ColorApiView(ListCreateAPIView):
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
    permission_classes = [AllowAny]

class CharacteristikDetailView(RetrieveAPIView):
    queryset = CharacteristikTopik.objects.all()
    serializer_class = CharacteristikSerializer
    permission_classes = [AllowAny]
    
