from django.shortcuts import render
from rest_framework.viewsets import generics
from app_collection.models import NewCollection, Recommendations
from app_collection.serializers import (NewCollectionCreateSerializer, NewCollectionListSerializer,
RecommendationCreateSerializer, RecommendationListSerializer)



class NewCollectionCreateApiView(generics.CreateAPIView):
    queryset = NewCollection.objects.all()
    serializer_class = NewCollectionCreateSerializer



class NewCollectionListApiView(generics.ListAPIView):
    queryset = NewCollection.objects.all()
    serializer_class = NewCollectionListSerializer



class NewCollectionRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewCollection.objects.all()
    serializer_class = NewCollectionCreateSerializer
    lookup_field = "id"








class RecommendationListApiView(generics.ListAPIView):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationListSerializer


class RecommendationCreateApiView(generics.CreateAPIView):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationCreateSerializer



class RecommendationRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationCreateSerializer
    lookup_field = "id"