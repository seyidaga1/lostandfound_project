from rest_framework import serializers
from .models import Pet,Favorite
from .models import ContactMessage

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




class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'full_name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']