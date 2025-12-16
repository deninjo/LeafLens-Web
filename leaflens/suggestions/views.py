from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Suggestion
from .serializers import SuggestionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class SuggestionViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - POST (user submits)
    - GET (list suggestions)
    - PATCH/PUT (admin approves/rejects)
    """
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer

    # only authenticated users can view and post suggestions
    permission_classes = [IsAuthenticated]  # Only logged-in users

    # Enable filtering, searching, ordering
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]  # browsable API UI/returns JSON
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering by disease, type, status
    # GET /api/suggestions/?disease=3
    # GET /api/suggestions/?type = prevention
    # GET /api/suggestions/?status = pending


    filterset_fields = ['disease', 'type', 'status']
    search_fields = ['suggestion']  # optional free-text search - GET /api/suggestions/?search=rotation
    ordering_fields = ['created_at']
    ordering = ['-created_at'] # GET /api/suggestions/?ordering=created_at

    def perform_create(self, serializer):
        # Automatically link suggestion to current user
        serializer.save(user=self.request.user)

