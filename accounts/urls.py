from django.urls import path
from .views import ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # login
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
]