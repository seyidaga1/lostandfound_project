from rest_framework import serializers
from .models import Pet,Favorite

class PetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Pet
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'pet']