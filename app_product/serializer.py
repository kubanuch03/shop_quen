from rest_framework import serializers
from app_product.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    subcategory_title = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    def get_subcategory_title(self, obj):
        return obj.subcategory.title if obj.subcategory.title else None

    def get_color(self, obj):
        colors = obj.color.all()
        return [color.colors for color in colors]

    def get_size(self, obj):
        sizes = obj.size.all()
        return [size.sizes for size in sizes]

    class Meta:
        model = Product
        fields = ["subcategory",
                "subcategory_title",
                "title", 
                "price", 
                "description", 
                "brand", 
                "characteristics", 
                "is_any", 
                "images1", 
                "images2", 
                "images3", 
                "color",
                "size",
]
        

class ProductcreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id",
                "subcategory",
                "title", 
                "price", 
                "description", 
                "brand", 
                "characteristics", 
                "is_any", 
                "images1", 
                "images2", 
                "images3", 
                "color",
                "size",
]