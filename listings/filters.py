from django_filters import rest_framework as filters
from .models import Pet

class PetFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_age = filters.NumberFilter(field_name='age', lookup_expr='gte')
    max_age = filters.NumberFilter(field_name='age', lookup_expr='lte')

    class Meta:
        model = Pet
        fields = {
            'type': ['exact'],
            'breed': ['exact', 'icontains'],
            'gender': ['exact'],
            'status': ['exact'],
            'vaccinated': ['exact'],
            'city': ['exact', 'icontains'],
        }