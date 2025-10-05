from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pet,Favorite
from .serializers import PetSerializer,FavoriteSerializer
from .filters import PetFilter
from django.shortcuts import get_object_or_404
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Option 1: Separate Generic Views for each CRUD operation
class PetListView(generics.ListAPIView):
    """GET /api/pets/ - List all pets with filtering and search"""
    queryset = Pet.objects.all().order_by('-created_at')
    serializer_class = PetSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = {
        'type': ['exact'],
        'breed': ['exact', 'icontains'],
        'gender': ['exact'],
        'status': ['exact'],
        'price': ['gte', 'lte'],
        'age': ['gte', 'lte'],
        'vaccinated': ['exact'],
        'city': ['exact', 'icontains'],
    }
    
    search_fields = ['name', 'breed', 'description', 'city']
    ordering_fields = ['created_at', 'price', 'age', 'name']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        pets = self.get_queryset()
        stats = {
            "total": pets.count(),
            "adopting": pets.filter(status="adopting").count(),
            "selling": pets.filter(status="selling").count(),
            "breeding": pets.filter(status="breeding").count(),
            "urgent": pets.filter(is_urgent=True).count()
        }
        response.data = {
            "stats": stats,
            "pets": response.data
        }
        return response

class PetCreateView(generics.CreateAPIView):
    """POST /api/pets/create/ - Create a new pet"""
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetDetailView(generics.RetrieveAPIView):
    """GET /api/pets/{id}/ - Get a specific pet"""
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.AllowAny]


class PetUpdateView(generics.UpdateAPIView):
    """PUT/PATCH /api/pets/{id}/update/ - Update a pet"""
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {'error': 'You do not have permission to update this pet. Only the owner can update.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {'error': 'You do not have permission to update this pet. Only the owner can update.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)


class PetDeleteView(generics.DestroyAPIView):
    """DELETE /api/pets/{id}/delete/ - Delete a pet"""
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response(
                {'error': 'You do not have permission to delete this pet. Only the owner can delete.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


# Option 2: Custom APIViews for more control
class PetManagementView(APIView):
    """Custom view for specific pet management operations"""
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get(self, request, pk=None):
        """GET /api/pets/manage/{id}/ - Get pet details"""
        try:
            pet = Pet.objects.get(pk=pk)
            serializer = PetSerializer(pet)
            return Response(serializer.data)
        except Pet.DoesNotExist:
            return Response(
                {'error': 'Pet not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, pk=None):
        """PUT /api/pets/manage/{id}/ - Full update"""
        try:
            pet = Pet.objects.get(pk=pk)
            if pet.owner != request.user:
                return Response(
                    {'error': 'Only the owner can update this pet'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = PetSerializer(pet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Pet.DoesNotExist:
            return Response(
                {'error': 'Pet not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, pk=None):
        """DELETE /api/pets/manage/{id}/ - Delete pet"""
        try:
            pet = Pet.objects.get(pk=pk)
            if pet.owner != request.user:
                return Response(
                    {'error': 'Only the owner can delete this pet'},
                    status=status.HTTP_403_FORBIDDEN
                )
            pet.delete()
            return Response(
                {'message': 'Pet deleted successfully'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Pet.DoesNotExist:
            return Response(
                {'error': 'Pet not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


# Keep utility endpoints separate
class PetUtilityViewSet(viewsets.GenericViewSet):
    """Utility endpoints that don't fit CRUD pattern"""
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_status(self, request, pk=None):
        """POST /api/pets/utils/{id}/change_status/"""
        pet = self.get_object()
        
        if pet.owner != request.user:
            return Response(
                {'error': 'Only the owner can change the status'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        # Note: Fix the reference to Pet.STATUS_CHOICES instead of Item.ITEM_STATUS
        if new_status not in dict(Pet.STATUS_CHOICES):  # Assuming Pet has STATUS_CHOICES
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        pet.status = new_status
        pet.save()
        
        return Response({'status': 'Pet status updated successfully'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_pets(self, request):
        """GET /api/pets/utils/my_pets/"""
        pets = Pet.objects.filter(owner=request.user)
        serializer = self.get_serializer(pets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available_pets(self, request):
        """GET /api/pets/utils/available_pets/"""
        pets = Pet.objects.filter(status='available')
        serializer = self.get_serializer(pets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def price_ranges(self, request):
        """GET /api/pets/utils/price_ranges/"""
        queryset = Pet.objects.all()
        min_price = queryset.exclude(price__isnull=True).order_by('price').values_list('price', flat=True).first()
        max_price = queryset.exclude(price__isnull=True).order_by('-price').values_list('price', flat=True).first()
        
        return Response({
            'min_price': min_price,
            'max_price': max_price
        })


# Option 3: Separate ViewSets for different concerns
class PetListAPIView(generics.ListAPIView):
    """Read-only operations for public access"""
    queryset = Pet.objects.order_by('-created_at')
    serializer_class = PetSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = {
        'type': ['exact'],
        'breed': ['exact', 'icontains'],
        'gender': ['exact'],
        'price': ['gte', 'lte'],
        'age': ['gte', 'lte'],
        'vaccinated': ['exact'],
        'city': ['exact', 'icontains'],
    }
    
    search_fields = ['name', 'breed', 'description', 'city']
    ordering_fields = ['created_at', 'price', 'age', 'name']


class PetOwnerViewSet(viewsets.ModelViewSet):
    """Full CRUD operations for pet owners"""
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Option 4: Function-based views for maximum control
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_pets(request):
    """GET /api/pets/list/ - List all available pets"""
    pets = Pet.objects.filter(status='available').order_by('-created_at')
    serializer = PetSerializer(pets, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_pet(request):
    """POST /api/pets/add/ - Create a new pet"""
    serializer = PetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_pet(request, pk):
    """GET /api/pets/detail/{id}/ - Get specific pet"""
    try:
        pet = Pet.objects.get(pk=pk)
        serializer = PetSerializer(pet)
        return Response(serializer.data)
    except Pet.DoesNotExist:
        return Response(
            {'error': 'Pet not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_pet(request, pk):
    """PUT/PATCH /api/pets/edit/{id}/ - Update pet"""
    try:
        pet = Pet.objects.get(pk=pk)
        if pet.owner != request.user:
            return Response(
                {'error': 'Only the owner can update this pet'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        partial = request.method == 'PATCH'
        serializer = PetSerializer(pet, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Pet.DoesNotExist:
        return Response(
            {'error': 'Pet not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_pet(request, pk):
    """DELETE /api/pets/remove/{id}/ - Delete pet"""
    try:
        pet = Pet.objects.get(pk=pk)
        if pet.owner != request.user:
            return Response(
                {'error': 'Only the owner can delete this pet'},
                status=status.HTTP_403_FORBIDDEN
            )
        pet.delete()
        return Response(
            {'message': 'Pet deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )
    except Pet.DoesNotExist:
        return Response(
            {'error': 'Pet not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class AddFavoriteView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)

        if not created:
            return Response({"message": "Already in favorites"}, status=status.HTTP_200_OK)

        return Response({"message": "Pet added to favorites"}, status=status.HTTP_201_CREATED)


class RemoveFavoriteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pet_id):
        favorite = get_object_or_404(Favorite, user=request.user, pet_id=pet_id)
        favorite.delete()
        return Response({"message": "Pet removed from favorites"}, status=status.HTTP_200_OK)
    
@method_decorator(csrf_exempt, name='dispatch')
class ContactCreateView(generics.CreateAPIView):
    """Handle contact form submission"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Debug print
        
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            print("Message saved successfully")  # Debug print
            return Response(
                {'message': 'Mesajınız uğurla göndərildi!'},
                status=status.HTTP_201_CREATED
            )
        
        print("Validation errors:", serializer.errors)  # Debug print
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)