# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router for utility endpoints
router = DefaultRouter()
router.register(r'pets/utils', views.PetUtilityViewSet, basename='pet-utils')
router.register(r'pets/owner', views.PetOwnerViewSet, basename='pet-owner')

urlpatterns = [
    # Option 1: Generic Views - Separate CRUD endpoints
    path('pets/', views.PetListView.as_view(), name='pet-list'),
    path('pets/create/', views.PetCreateView.as_view(), name='pet-create'),
    path('pets/<int:pk>/', views.PetDetailView.as_view(), name='pet-detail'),
    path('pets/<int:pk>/update/', views.PetUpdateView.as_view(), name='pet-update'),
    path('pets/<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet-delete'),
    
    # Option 2: Custom Management View
    path('pets/manage/<int:pk>/', views.PetManagementView.as_view(), name='pet-manage'),
    
    # Option 3: Function-based views with custom endpoints
    path('pets/list/', views.list_pets, name='pet-list-fbv'),
    path('pets/add/', views.create_pet, name='pet-create-fbv'),
    path('pets/detail/<int:pk>/', views.get_pet, name='pet-detail-fbv'),
    path('pets/edit/<int:pk>/', views.update_pet, name='pet-update-fbv'),
    path('pets/remove/<int:pk>/', views.delete_pet, name='pet-delete-fbv'),
    
    path('favorites/', views.FavoriteListView.as_view(), name="favorite-list"),
    path('favorites/<int:pet_id>/', views.AddFavoriteView.as_view(), name="favorite-add"),
    path('favorites/<int:pet_id>/remove/', views.RemoveFavoriteView.as_view(), name="favorite-remove"),

    # ViewSet-based utility and specialized endpoints
    path('', include(router.urls)),
]

# Alternative URL structure - Version-based separation
urlpatterns_versioned = [
    # V1 - Basic CRUD (backwards compatibility)
    path('v1/pets/', views.PetListView.as_view(), name='pet-list-v1'),
    path('v1/pets/create/', views.PetCreateView.as_view(), name='pet-create-v1'),
    path('v1/pets/<int:pk>/', views.PetDetailView.as_view(), name='pet-detail-v1'),
    
    # V2 - Management operations
    path('v2/pets/manage/<int:pk>/', views.PetManagementView.as_view(), name='pet-manage-v2'),
    
    # V3 - Specialized endpoints
    path('v3/', include(router.urls)),
]

# Alternative URL structure - Action-based separation
urlpatterns_action_based = [
    # Read operations
    path('pets/browse/', views.PetListView.as_view(), name='pet-browse'),
    path('pets/view/<int:pk>/', views.PetDetailView.as_view(), name='pet-view'),
    
    # Write operations
    path('pets/add/', views.PetCreateView.as_view(), name='pet-add'),
    path('pets/modify/<int:pk>/', views.PetUpdateView.as_view(), name='pet-modify'),
    path('pets/remove/<int:pk>/', views.PetDeleteView.as_view(), name='pet-remove'),
    
    # Utility operations
    path('', include(router.urls)),
]