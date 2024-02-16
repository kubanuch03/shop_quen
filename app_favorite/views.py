from rest_framework import permissions, generics, response, status

from django.views import View
from django.http import JsonResponse

from .models import Favorite
from .serializers import FavoriteSerializer
from .permissions import IsUserOrAdmin


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