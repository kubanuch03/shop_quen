from decouple import config

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


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email",)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data["email"],
            token_auth=get_random_string(14),
        )

        current_site = get_current_site(self.context["request"])
        domain = current_site.domain
        protocol = "https" if self.context["request"].is_secure() else "http"
        confirmation_link = reverse(
            "users:confirm_email", kwargs={"token": user.token_auth}
        )

        subject = "Подтверждение почты"

        # message = f"""Подтвердите почту по ссылке: \n\n{protocol}://{domain}{confirmation_link}\nВаши данные:\n почта: {client.email}\n пароль: {validated_data["password"]}"""
        html_message = render_to_string('app_users/confirm_email.html', {
                    'protocol': protocol,
                    'domain': domain,
                    'confirmation_link': confirmation_link,
                    'user_email': user.email,
                })
        text_message = strip_tags(html_message)

        # from_email = config("EMAIL_HOST_USER")
        # to_email = validated_data["email"]
        # send_mail(subject, html_message, from_email, [to_email], fail_silently=False)

        email = EmailMultiAlternatives(subject, text_message, from_email=config("EMAIL_HOST_USER"), to=[validated_data["email"]])
        email.attach_alternative(html_message, "text/html")  # Установите альтернативный контент как HTML
        email.send()
        make_password(validated_data["password"])

        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("full_name", "phone_number", "password", "password2", )

    def validate(self, attrs):
        if attrs.get("password") or attrs.get("password2"):
            if attrs["password"] != attrs["password2"]:
                raise serializers.ValidationError(
                    {"password": "Пароль не совпадает, попробуйте еще раз"}
                )
        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            if attr == "password":
                instance.set_password(value)
        instance.save()
        return instance


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password")
