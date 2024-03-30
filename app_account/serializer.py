from rest_framework import serializers
from app_user.models import CustomUser
from app_account.models import PaymentMethod, History, Deliver


class ChangeUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'full_name',
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



class DeliverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliver
        fields = ['types', 'location']


class HistoryListSerializer(serializers.ModelSerializer):
    deliver = DeliverSerializer()
    class Meta:
        model = History
        fields = ['products', 'user', 'price', 'lastname', 'firstname', 'deliver', 'payment_type', 'status']


class HistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['products', 'user', 'price', 'lastname', 'firstname', 'deliver', 'payment_type', 'status']

 
    



