from django.shortcuts import render

# viewset
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Disease
from .serializers import DiseaseSerializer

# filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import renderers
from .filters import DiseaseFilter

# Create your views here.

# viewSet Diseases(wrap multiple CBV methods into one class)
# LIST ALL DISEASES x RETRIEVE ONE DISEASE
class DiseaseViewSet(ReadOnlyModelViewSet):
    """Performing read-only operations on Diseases"""
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

    # Enable filtering, searching, ordering
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]  # browsable API UI/returns JSON
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # 1. Filtering
    filterset_class = DiseaseFilter

    # 2. Searching
    search_fields = ['name', 'scientific_name']       # Full-text search

    # 3. Ordering
    ordering_fields = ['name', 'scientific_name']     # Sorting
    ordering = ['name']    # default sort

