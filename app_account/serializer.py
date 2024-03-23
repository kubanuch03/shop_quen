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


class SendResetCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=30)
    confirming_new_password = serializers.CharField(max_length=30)

    class Meta:
        fields = ['new_password', 'confirming_new_password']    