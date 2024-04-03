from rest_framework import serializers
import re
from app_product.models import Product, Color, Size, CharacteristikTopik

class SizeSerializer(serializers.ModelSerializer):
    sizes = serializers.CharField()

    class Meta:
        model = Size
        fields = ["id", "sizes"]

    def validate(self, attrs):
        sizes = attrs['sizes']

        if not re.match("^[a-zA-Z]+$", sizes):
            raise serializers.ValidationError(
                'размер должен содержать только английские буквы'
            )

        attrs['sizes'] = sizes.upper()

        return attrs


class ColorSerializer(serializers.ModelSerializer):
    colors = serializers.CharField()

    class Meta:
        model = Color
        fields = ['id', 'colors']

    def validate(self, attrs):
        colors = attrs['colors']

        if not re.match("^[a-zA-Z]+$", colors):
            raise serializers.ValidationError(
                'размер должен содержать только английские буквы'
            )

        attrs['colors'] = colors.upper()

        return attrs



class CharacteristikSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharacteristikTopik
        fields = ['id','title','value']



class ProductListSerializer(serializers.ModelSerializer):
    color =ColorSerializer(many=True)
    characteristics =CharacteristikSerializer(many=True)
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
                "is_favorite",
                
]
    def to_representation(self, instance):
        data_product = super().to_representation(instance)        
        data_product['size'] = SizeSerializer(instance.size.all(), many=True).data
        data_product['color'] = ColorSerializer(instance.color.all(),many=True).data
        data_product['characteristics'] = CharacteristikSerializer(instance.characteristics.all(),many=True).data
        
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
        

