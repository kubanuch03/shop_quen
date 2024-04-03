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
    
    def create(self, validated_data):
        title = validated_data['title']
        value = validated_data['value']

        if title.isdigit() or value.isdigit():
            raise serializers.ValidationError({"error":"title,value cannot contain is digit!"})
        return super().create(validated_data)
    
    


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
    discount = serializers.CharField(required=False)

    def apply_discount_to_price(self, price, discount):
        if '%' in discount: 
            discount_percentage = int(discount.replace('%', ''))
            if discount_percentage > 0 and discount_percentage <= 100:
                discounted_price = price - (price * discount_percentage) // 100
                return discounted_price
        else:
            discount_value = int(discount)
            if discount_value > 0:
                discounted_price = price - discount_value
                return discounted_price
        return price

    def create(self, validated_data):
        discount = validated_data.get('discount')
        price = validated_data['price']
        title = validated_data['title']
        brand = validated_data['brand']
        description = validated_data['description']
        
        # Применяем скидку к цене, если указана
        if discount is not None:
            discounted_price = self.apply_discount_to_price(price, discount)
            validated_data['price'] = discounted_price
        
        # Проверяем, что цена положительная
        if price <= 0:
            raise serializers.ValidationError({"price": "Price must be a positive integer."})
        
        # Проверяем, что title, brand и description не содержат только цифры
        if (title.isdigit() or brand.isdigit() or description.isdigit()):
            raise serializers.ValidationError({"error":"title, brand, description cannot contain only digits."})

        # Проверяем, что в title и brand есть хотя бы одна буква
        if not any(c.isalpha() for c in title) or not any(c.isalpha() for c in brand):
            raise serializers.ValidationError({"error": "title and brand must contain at least one letter."})

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
        




