from django.urls import path
from app_collection.views import *


urlpatterns = [
    path('list/collection/', NewCollectionListApiView.as_view()),
    path('create/collection/', NewCollectionCreateApiView.as_view()),
    path('rud/collection/<int:id>/', NewCollectionRUDApiView.as_view()),


    path('list/recommendation/', RecommendationListApiView.as_view()),
    path('detail/recommendation/<pk>/', RecommendationDetailApiView.as_view()),
    path('create/recommendation/', RecommendationCreateApiView.as_view()),
    path('rud/recommendation/<int:id>/', RecommendationRUDApiView.as_view()),



    path('delete/all/collection/', NewCollectionDeleteAllApiView.as_view()),

]