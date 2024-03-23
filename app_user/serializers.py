from decouple import config
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags

from rest_framework import serializers
from .models import CustomUser


class ConfirmEmailSerializer(serializers.Serializer):
    token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "phone_number",
            "password",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password"].strip() != attrs["password2"].strip():
            raise serializers.ValidationError(
                {"password": "Пароль не совпадает, попробуйте еще раз"}
            )
        if len(attrs["password"].strip()) and len(attrs["password2"].strip()) <8:
            raise serializers.ValidationError(
                ("Password must be at least 8 characters long."),
                code='password_too_short',
            )
        return attrs

    def create(self, validated_data):
        code = ''.join(random.choices('0123456789', k=6))  
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data.get("username", ""),
            password=validated_data["password"],
            code=code  #
        )

        subject = "Код подтверждения"
        message = f"Ваш код подтверждения: {code}"
        email = EmailMultiAlternatives(subject, message, to=[validated_data["email"]])
        email.send()

        return user
    
class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password")

class VerifyUserCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6, required=True)

    def validate_code(self, value):
        """
        Validate the code field.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Code must contain only digits.")
        return value