from rest_framework import serializers
import re
from app_product.models import Product, Color, Size, CharacteristikTopik, IsFavorite

class SizeSerializer(serializers.ModelSerializer):
    sizes = serializers.CharField()

    class Meta:
        model = Size
        fields = ["id", "sizes"]

    def validate(self, attrs):
        sizes = attrs['sizes']

        if not (re.match("^[a-zA-Z]+$", sizes) or re.match("^\d{1,2}$", sizes)):
            raise serializers.ValidationError(
                'размер должен содержать только английские буквы или цифры до двух значений (максимум 99)'
            )
        
        if re.match("^\d{1,2}$", sizes):
            sizes = int(sizes)
            if sizes > 99:
                raise serializers.ValidationError(
                    'максимальное значение для числового размера - 99'
                )

        attrs['sizes'] = sizes.upper()
        if Size.objects.filter(sizes=attrs['sizes']).exists():
            raise serializers.ValidationError('sizes is already.')
        attrs['sizes'] = str(sizes).upper() if isinstance(sizes, str) else str(sizes)

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
        if Color.objects.filter(colors=attrs['colors']).exists():
            raise serializers.ValidationError('color is already.')

        return attrs



class CharacteristikSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharacteristikTopik
        fields = ['id','title','value']
    
    def create(self, validated_data):
        title = validated_data['title']
        # value = validated_data['value']

        if title.isdigit():
            raise serializers.ValidationError({"error":"title cannot contain is digit!"})
        return super().create(validated_data)



class IsFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = IsFavorite
        fields = ['id','user']
    

class IsFavoriteDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = IsFavorite
        fields = ['id','user','product',]

        
#=====  Product   ===================================================================================================================================================================

class ProductListSerializer(serializers.ModelSerializer):
    is_favorite =IsFavoriteSerializer(many=True)
    color =ColorSerializer(many=True)
    size = SizeSerializer(many=True)
    characteristics =CharacteristikSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'subcategory',
            'description',
            'brand',
            'characteristics',
            'is_any',
            'discount',
            'created_at',
            'title',
            'price',
            'is_favorite',
            'images1',
            'images2',
            'images3',
            'subcategory',
            "color",
            "size",
            ]
    def to_representation(self, instance):
        data_product = super().to_representation(instance)        
        data_product['is_favorite'] = IsFavoriteSerializer(instance.is_favorite.all(),many=True).data
        data_product['size'] = SizeSerializer(instance.size.only('sizes'), many=True).data
        data_product['color'] = ColorSerializer(instance.color.only('colors'),many=True).data
        data_product['characteristics'] = CharacteristikSerializer(instance.characteristics.only('title'),many=True).data
        
        return data_product   


class ProductDetailSerializer(serializers.ModelSerializer):
    color =ColorSerializer(many=True)
    size = SizeSerializer(many=True)
    characteristics =CharacteristikSerializer(many=True)
    is_favorite =IsFavoriteSerializer(many=True)
    
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
                "is_favorite",
                "images1", 
                "images2", 
                "images3", 
                "color",
                "size",
                "discount",
                
                ]

    

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('subcategory').prefetch_related('color', 'characteristics', 'size')
        return queryset
    
    def to_representation(self, instance):
        data_product = super().to_representation(instance)        
        data_product['size'] = SizeSerializer(instance.size.only('sizes'), many=True).data
        data_product['color'] = ColorSerializer(instance.color.only('colors'),many=True).data
        data_product['characteristics'] = CharacteristikSerializer(instance.characteristics.only('title'),many=True).data
        data_product['is_favorite'] = IsFavoriteSerializer(instance.is_favorite.all(),many=True).data
        
        return data_product



class ProductcreateSerializer(serializers.ModelSerializer):
    discount = serializers.IntegerField(required=False)

    def apply_discount_to_price(self, price, discount):
        
        discount_value = int(discount)
        discounted_price = price - discount_value
        return discounted_price
    

    # def to_internal_value(self, data):
    #     # Создаем копию QueryDict
    #     mutable_data = data.copy()
    #     # Переводим поля, связанные с pk, из int в str
    #     if 'subcategory' in mutable_data:
    #         mutable_data['subcategory'] = str(mutable_data['subcategory'])
    #     if 'color' in mutable_data:
    #         mutable_data['color'] = str(mutable_data['color'])
        # if 'size' in mutable_data:
        #     mutable_data['size'] = str(mutable_data['size'])

        # return super().to_internal_value(mutable_data)

    def create(self, validated_data):
        discount = validated_data.get('discount')
        price = validated_data['price']
        title = validated_data['title']
        brand = validated_data['brand']
        description = validated_data['description']
        
        if discount is not None and discount <= 0:
            raise serializers.ValidationError({"discount": "Скидка должна быть положительным целым числом."})
        
        if discount is not None:
            discounted_price = self.apply_discount_to_price(price, discount)
            validated_data['price'] = discounted_price
        
        if price <= 0:
            raise serializers.ValidationError({"price": "Price must be a positive integer."})
        
        if (title.isdigit() or brand.isdigit() or description.isdigit()):
            raise serializers.ValidationError({"error":"title, brand, description cannot contain only digits."})

        if not any(c.isalpha() for c in title) or not any(c.isalpha() for c in brand):
            raise serializers.ValidationError({"error": "title and brand must contain at least one letter."})

        return super().create(validated_data)

    
    
    class Meta:
        model = Product
        fields = [
                "id",
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
        



