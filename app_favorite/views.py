from rest_framework import permissions, generics, response, status


from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.core.cache import cache

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
    
    @method_decorator(cache_page(100))  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    


class FavoriteCreateApiView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = self.request.data['product']
        try:
            product = Product.objects.get(pk=product_id)
            if Favorite.objects.filter(user=request.user, product=product).exists():
                return response.Response({"error": "Product  is already in favorites"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Favorite.DoesNotExist:
            return response.Response({"error":"Product does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        favorite = Favorite.objects.create(user=request.user,product=product)
        favorite.is_favorite=True
        favorite.save()

        serializer = self.get_serializer(favorite)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)






        

    


class FavoriteDetailApiView(generics.RetrieveAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60))  
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


    @method_decorator(cache_page(60))  
    def get_queryset(self):
        return Favorite.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.filter(id=self.kwargs[self.lookup_field]).first()
        if obj is None:
            raise Http404("Product does not exist")
        return obj
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # Удаляем соответствующий кеш по ключу
        cache_key = f'favorite_detail_{instance.id}'
        cache.delete(cache_key)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteUpdateApiView(generics.UpdateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.AllowAny]