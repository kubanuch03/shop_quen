from rest_framework import serializers
from  .models import Banner, TopikBaner


class BannerCRUDserializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["topik_baner"]


class TopikBannerCRUDserializer(serializers.ModelSerializer):
    class Meta:
        model = TopikBaner
        fields = ["id", "name", "images"]