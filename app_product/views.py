from app_product.serializer import ProductListSerializer, ProductcreateSerializer
from app_product.models import Product
from app_product.filters import PriceRangeFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from app_product.permissions import IsCreatorOrAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated


class ListAllProductApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [PriceRangeFilter, SearchFilter]
    permission_classes = [AllowAny, ]


class CreateProductApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    # permission_classes = [IsAuthenticated, ]



class ProductDeleteApiView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    lookup_field = "id"
    permission_classes = [IsCreatorOrAdmin, ]



class ProductUpdateApiView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductcreateSerializer
    lookup_field = "id"
    # permission_classes = [IsAuthenticated, ]

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.price = serializer.apply_discount_to_price(instance.price, serializer.validated_data.get('discount', 0))
        instance.save()


class ListOneProducApiView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, id):
        products = Product.objects.filter(id=id)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    

class ProductBySubCategory(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, subcategory_id):
        products = Product.objects.filter(subcategory_id=subcategory_id)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)