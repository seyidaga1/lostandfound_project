from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django_countries.fields import CountryField
from .phone_codes import COUNTRY_PHONE_CODES

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    location = CountryField(blank=True, null=True)
    last_seen = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.location and not self.phone:
            code = getattr(self.location, "code", self.location)
            self.phone = COUNTRY_PHONE_CODES.get(code, "")
        super().save(*args, **kwargs)
