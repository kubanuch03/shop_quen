from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (ListAPIView,
CreateAPIView, RetrieveUpdateDestroyAPIView)
from app_category.models import Category, SubCategory
from app_category.serializer import (CategoryListRUDSerializer, 
CategoryCreateSerializer, SubCategoryListSerializer, SubCategoryCreateSerializer)
from app_product.filters import SearchFilter



class CategoryAllListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListRUDSerializer
    filter_backends = [SearchFilter]



class ListOneCategoryApiView(APIView):
    def get(self, request, id):
        category = Category.objects.filter(id=id)
        serializer = CategoryListRUDSerializer(category, many=True)
        return Response(serializer.data)



class CategoryCreateApiView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer



class CategoryRUDApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListRUDSerializer
    lookup_field = "id"

'=============================================== Category ======================================================= '


class SubCategoryAllListApiView(ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSerializer
    filter_backends = [SearchFilter]


class ListOneSubCategoryApiView(APIView):
    def get(self, request, id):
        subcategory = SubCategory.objects.filter(id=id)
        serializer = CategoryListRUDSerializer(subcategory, many=True)
        return Response(serializer.data)


class SubCategoryCreateApiView(CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializer


class SubCategoryRUDApiView(RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSerializer
    lookup_field = "id"



class CategoryBySubCategory(APIView):
    def get(self, request, category_id):
        subcategory = SubCategory.objects.filter(category_id=category_id)
        serializer = SubCategoryListSerializer(subcategory, many=True)
        return Response(serializer.data)