from rest_framework import permissions, generics, response, status

from django.views import View
from django.http import JsonResponse

from .models import Favorite
from .serializers import FavoriteSerializer
from .permissions import IsUserOrAdmin

from app_product.models import Product

class FavoriteListApiView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user)
        return Favorite.objects.none()

    


class FavoriteCreateApiView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = self.request.data['product']
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
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


class FavoriteDeleteApiView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.AllowAny]


class FavoriteUpdateApiView(generics.UpdateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.AllowAny]