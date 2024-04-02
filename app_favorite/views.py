from rest_framework import permissions, generics, response, status


from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.cache import cache_page

from .models import Favorite
from .serializers import FavoriteSerializer
from .permissions import IsUserOrAdmin

from app_product.models import Product

class FavoriteListApiView(generics.ListAPIView):
    queryset = Favorite.objects.all().select_related('product').prefetch_related('user',)
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user)
        return Favorite.objects.none()
    
    @method_decorator(cache_page(60*60))  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    


class FavoriteCreateApiView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = self.request.data['product']
        try:
            product = Favorite.objects.get(pk=product_id)
        except Favorite.DoesNotExist:
            return response.Response({"error":"Product does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        favorite = Favorite.objects.create(user=request.user,product=product)
        product.is_favorite=True
        product.save()

        serializer = self.get_serializer(favorite)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)



        

    


class FavoriteDetailApiView(generics.RetrieveAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(id=self.kwargs[self.lookup_field]).first()
        if obj is None:
            raise Http404("Product does not exist")
        return obj

class FavoriteDeleteApiView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Favorite.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(id=self.kwargs[self.lookup_field]).first()
        if obj is None:
            raise Http404("Product does not exist")
        return obj


class FavoriteUpdateApiView(generics.UpdateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.AllowAny]