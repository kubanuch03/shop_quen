from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ['id','user','product','created_at',]

