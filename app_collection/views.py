from django.shortcuts import render
from rest_framework.viewsets import generics
from app_collection.models import NewCollection, Recommendations
from app_collection.serializers import (NewCollectionCreateSerializer, NewCollectionListSerializer,
RecommendationCreateSerializer, RecommendationListSerializer)

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class NewCollectionCreateApiView(generics.CreateAPIView):
    queryset = NewCollection.objects.all()
    serializer_class = NewCollectionCreateSerializer





class NewCollectionListApiView(generics.ListAPIView): #Было 4 SQL запроса стало 3
    queryset = NewCollection.objects.all().prefetch_related('product')
    serializer_class = NewCollectionListSerializer



class NewCollectionRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewCollection.objects.all()
    serializer_class = NewCollectionCreateSerializer
    lookup_field = "id"


    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # Если в запросе передан пустой массив для поля 'product', очистить поле
        if 'product' in request.data and not request.data['product']:
            instance.product.clear()
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)




class NewCollectionDeleteAllApiView(APIView):
    serializer_class = None
    def delete(self, request, *args, **kwargs):
        try:
            NewCollection.objects.all().delete()
            return Response({'detail': 'All objects deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'detail': 'Failed to delete all objects'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RecommendationListApiView(generics.ListAPIView):
    queryset = Recommendations.objects.all()#.prefetch_related('product')  #Было 4 SQL запроса стало 3
    serializer_class = RecommendationListSerializer

class RecommendationDetailApiView(generics.RetrieveAPIView):
    queryset = Recommendations.objects.all()#.prefetch_related('product')  #Было 4 SQL запроса стало 3
    serializer_class = RecommendationListSerializer


class RecommendationCreateApiView(generics.CreateAPIView):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationCreateSerializer



class RecommendationRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationCreateSerializer
    lookup_field = "id"