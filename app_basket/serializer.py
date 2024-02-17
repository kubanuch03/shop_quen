from rest_framework import serializers
from .models import BasketItem

class BasketItemSerializer(serializers.ModelSerializer):
    product_title = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()

    def get_product_title(self, obj):
        return obj.product.title

    def get_product_price(self, obj):
        return obj.product.price
    
    class Meta:
        model = BasketItem
        fields = ('id', 'product', 'quantity', 'product_title', 'product_price')
