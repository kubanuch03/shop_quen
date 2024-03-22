from rest_framework import serializers
from app_user.models import CustomUser
from app_account.models import PaymentMethod


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
        