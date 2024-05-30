from rest_framework import serializers
from app_user.models import CustomUser
from app_account.models import PaymentMethod, History, ProductInstance, Color, Size
from app_product.serializer import ProductDetailSerializer, SizeSerializer, ColorSerializer
from typing import Any

class ChangeUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'full_name',
            "phone_number",
        )


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "password",
            "phone_number",

        )


class HistoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
        )



class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['text']


class SendResetCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=30)
    confirming_new_password = serializers.CharField(max_length=30)

    class Meta:
        fields = ['new_password', 'confirming_new_password']    


from app_product.models import Product


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ["id", "discount", "price",  "images1", "images2", "images3"]





class HistoryListSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    user = HistoryUserSerializer()
    class Meta:
        model = History
        fields = ['id', 'products', 'user', 'price', 'lastname', 'firstname', 'types', 'location', 'payment_type', 'status', 'delivery_date']

    def to_representation(self, instance):
        data_product = super().to_representation(instance)        
        data_product['products'] = ProductInstanceSerializer(instance.products.all(),many=True).data
        
        return data_product  
    

    def get_products(self, obj: Any) -> Any:
        products_queryset = obj.products.all()
        products_data = ProductInstanceSerializer(products_queryset, many=True).data
        return products_data






class ProductInstanceSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = ProductInstance
        fields = ['product', 'color', 'size']

    
    def to_representation(self, instance):
        data_product = super().to_representation(instance)        
        data_product['product'] = ProductDetailSerializer(instance.product).data
        data_product['color'] = ColorSerializer(instance.color).data
        data_product['size'] = SizeSerializer(instance.size).data
        
        return data_product 

class HistoryCreateSerializer(serializers.ModelSerializer):
    products = ProductInstanceSerializer(many=True)
 
    class Meta:
        model = History
        fields = ['id','products','user', 'price', 'lastname', 'firstname', 'types', 'location', 'payment_type', 'status', 'delivery_date']
    
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        history = History.objects.create(**validated_data)
        for product_data in products_data:
            product_instance = ProductInstance.objects.create(history=history, **product_data)
            history.products.add(product_instance)
        return history


    # def create(self, validated_data):
    #     instance = History.objects.create(**validated_data)
    #     print(f"DATA: {instance}")
    #     return instance
    
    # def validate_products(self, value):
    #     # Преобразуем данные продуктов в нужный формат
    #     transformed_products = []
    #     for product_id in value:
    #         transformed_product = {
    #             "Id": product_id,
    #             "sizes": 1,  # Значение по умолчанию для sizes
    #             "colors": 1  # Значение по умолчанию для colors
    #         }
    #         transformed_products.append(transformed_product)
    #     return transformed_products

    # def create(self, validated_data):
    #     # Переопределяем метод create для обработки сохранения данных
    #     products_data = validated_data.pop('products')
    #     history = History.objects.create(**validated_data)
    #     for product_data in products_data:
    #         Product.objects.create(history=history, **product_data)
    #     return history
    
