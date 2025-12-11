import django_filters
from .models import Disease

class DiseaseFilter(django_filters.FilterSet):
    # We filter only simple fields (CharFields).
    class Meta:
        model = Disease
        fields = {
            'name': ['exact', 'icontains'],
            'scientific_name': ['exact', 'icontains'],
        }