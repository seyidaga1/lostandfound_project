from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# İstifadəçi token almaq üçün Simple JWT-dən hazır view istifadə et
# URL-də onu əlavə edəcəyik

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # İstifadəçi yalnız öz profilini görə və redaktə edə bilər
        return self.request.user