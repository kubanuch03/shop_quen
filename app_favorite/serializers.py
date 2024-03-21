from rest_framework import serializers

from .models import Favorite

from app_product.serializer import ProductListSerializer

class FavoriteSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(source='product.images1', read_only=True) 
    product_title = serializers.CharField(source='product.title', read_only=True) 
    class Meta:
        model = Favorite
        fields = ['id','user','product','product_title','product_image','created_at',]


