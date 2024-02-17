from app_product.serializer import ProductListSerializer, ProductcreateSerializer
from app_product.models import Product
from app_product.filters import PriceRangeFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from app_product.permissions import IsCreatorOrAdmin


class ListAllProductApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [PriceRangeFilter, SearchFilter]



class CreateProductApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer


class ProductDeleteApiView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    lookup_field = "id"
    permission_classes = [IsCreatorOrAdmin, ]



class ProductUpdateApiView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    lookup_field = "id"
    permission_classes = [IsCreatorOrAdmin, ]


class ListOneProducApiView(APIView):
    def get(self, request, id):
        products = Product.objects.filter(id=id)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    

class ProductBySubCategory(APIView):
    def get(self, request, subcategory_id):
        products = Product.objects.filter(subcategory_id=subcategory_id)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)