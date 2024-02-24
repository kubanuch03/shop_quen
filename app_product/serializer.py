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
        fields = ["id",
                "subcategory",
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
                "discount",
]
        

class ProductcreateSerializer(serializers.ModelSerializer):
    discount = serializers.IntegerField(required=False)

    def apply_discount_to_price(self, price, discount):
        if discount > 0 and discount <= 100:
            discounted_price = price - (price * discount) // 100
            return discounted_price
        else:
            return price

    def create(self, validated_data):
        discount = validated_data.get('discount')
        price = validated_data['price']
        if discount is not None:
            discounted_price = self.apply_discount_to_price(price, discount)
            validated_data['price'] = discounted_price
        return super().create(validated_data)

    
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
                "discount",
]
        
