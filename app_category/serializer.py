from rest_framework import serializers
from app_category.models import Category, SubCategory
from drf_spectacular.utils import extend_schema_field

class CategoryListRUDSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ["id", "title", "image"]



class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "image"]





"======================================= CategorySerializers ========================="

class SubCategoryListSerializer(serializers.ModelSerializer):
    category_title = serializers.SerializerMethodField()

    @extend_schema_field(str)
    def get_category_title(self, obj):
        return obj.category.title if obj.category.title else None

    class Meta:
        model = SubCategory
        fields = ["id", "title", "image", "category", "category_title"]



class SubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "title", "image", "category"]