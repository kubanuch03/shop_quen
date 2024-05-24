from rest_framework import serializers
from  .models import Banner, TopikBaner


class TopikBannerCRUDserializer(serializers.ModelSerializer):
    class Meta:
        model = TopikBaner
        fields = ["id", "name", "images"]


        
class BannerCRUDserializer(serializers.ModelSerializer):
    topik_baner = TopikBannerCRUDserializer(many=True,)

    class Meta:
        model = Banner
        fields = ["topik_baner"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['topik_baner']
    
    # def to_representation(self, instance):
    #     data_product = super().to_representation(instance)        
    #     data_product['topik_baner'] = TopikBannerCRUDserializer(instance.topik_baner.all(),many=True).data
        
    #     return data_product  

    # def update(self, instance, validated_data):
    #     # Extract nested topik_baner data
    #     topik_baner_data = validated_data.pop('topik_baner', None)

    #     # Update Banner instance
    #     instance = super().update(instance, validated_data)

    #     if topik_baner_data:
    #         # Clear existing many-to-many relations
    #         instance.topik_baner.clear()

    #         # Add new many-to-many relations
    #         for topik_data in topik_baner_data:
    #             topik_baner_instance, created = TopikBaner.objects.get_or_create(**topik_data)
    #             instance.topik_baner.add(topik_baner_instance)

    #     return instance
    
