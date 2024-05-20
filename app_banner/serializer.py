from rest_framework import serializers
from  .models import Banner, TopikBaner


class BannerCRUDserializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["topik_baner"]
    
    def to_representation(self, instance):
        data_product = super().to_representation(instance)        
        data_product['topik_baner'] = TopikBannerCRUDserializer(instance.topik_baner.all(),many=True).data
        
        return data_product  


class TopikBannerCRUDserializer(serializers.ModelSerializer):
    class Meta:
        model = TopikBaner
        fields = ["id", "name", "images"]