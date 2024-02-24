from rest_framework import serializers

from app_product.models import Product, Color, Size



class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','colors']

class ProductListSerializer(serializers.ModelSerializer):
    color =ColorSerializer(many=True)
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
    def to_representation(self, instance):
        data_product = super().to_representation(instance)        

        data_product['color'] = ColorSerializer(instance.color.all(),many=True).data
        
        return data_product

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
        