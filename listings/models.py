from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Pet(models.Model):
    PET_STATUS = (
        ('adopting', 'Adopting'),
        ('selling', 'Selling'),
        ('breeding', 'Breeding'),
    )
    
    PET_TYPE = (
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('fish', 'Fish'),
        ('other', 'Other')
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    # Basic Pet Information
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=PET_TYPE)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(help_text="Age in months")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    description = models.TextField()
    
    # Status and Price
    status = models.CharField(max_length=20, choices=PET_STATUS, default='adopting')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True ,default=0)
    
    # Health Information
    vaccinated = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    # Location
    city = models.CharField(max_length=100)
    
    # Ownership & Timestamps
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Images
    image = models.ImageField(upload_to='pets/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.breed} ({self.type})"

    class Meta:
        ordering = ['-created_at']

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        unique_together = ('user', 'pet')  # bir user eyni heyvanı təkrar favoritə sala bilməz

    def __str__(self):
        return f"{self.user.username} ❤️ {self.pet.name}"