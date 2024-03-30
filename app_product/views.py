from app_product.serializer import ProductListSerializer, ProductcreateSerializer, SizeSerializer, ColorSerializer, CharacteristikSerializer
from app_product.models import Product, Size, Color, CharacteristikTopik
from app_product.filters import PriceRangeFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from app_product.permissions import IsCreatorOrAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser



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
    permission_classes = [IsAdminUser, ]

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
    



class SizeApiView(ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser, ]


class SizeRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser, ]


class ColorApiView(ListCreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser, ]


class ColorRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser, ]


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
    