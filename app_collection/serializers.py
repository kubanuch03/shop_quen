from rest_framework import serializers
from app_collection.models import NewCollection, Recommendations
from app_product.models import Product
from drf_spectacular.utils import extend_schema
from django.conf import settings

from app_product.serializer import ProductListSerializer


class NewCollectionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewCollection
        fields = ["product"]










class RecommendationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = ["product"]

    
    

class RecommendationListSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = Recommendations
        fields = ["products"]
        
        def get_products(self, obj):
            request = self.context.get('request')
            products_queryset = obj.product.all()
            products_data = ProductListSerializer(products_queryset, many=True, context={'request': request}).data
            for product in products_data:
                product['images1'] = request.build_absolute_uri(settings.MEDIA_URL + product['images1'])
            return products_data


class NewCollectionListSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = NewCollection
        fields = ["products"]
        

    def get_products(self, obj):
        request = self.context.get('request')
        products_queryset = obj.product.all()
        products_data = ProductListSerializer(products_queryset, many=True, context={'request': request}).data
        for product in products_data:
            product['images1'] = request.build_absolute_uri(settings.MEDIA_URL + product['images1'])
        return products_data
    