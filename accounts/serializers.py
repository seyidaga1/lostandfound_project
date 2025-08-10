from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'location', 'phone')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)

        # Əgər telefon kodu boşdursa, location-a əsasən qoymaq istəyirsənsə, save metodu modeldə işləyəcək
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone', 'location')
        read_only_fields = ('email', 'username')  