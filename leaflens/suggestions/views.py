from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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

    # Control access per action
    def get_permissions(self):
        """
        ModelViewSet in DRF automatically provides a full set of CRUD endpoints:
        list() → GET /api/suggestions/
        retrieve() → GET /api/suggestions/<id>/
        create() → POST /api/suggestions/
        update() / partial_update() → PUT/PATCH /api/suggestions/<id>/
        destroy() → DELETE /api/suggestions/<id>/

        """
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            # Only admins can see / manage suggestions
            permission_classes = [IsAdminUser]
        else:
            # create (POST) → any authenticated user
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


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


    # Admin → sees everything, Farmer → sees nothing (via API)
    # DRF intentionally returns 403 instead of 401 for admin-only endpoints
    # 401 Unauthorized Meaning: “You are NOT authenticated. Please authenticate.” FE shows login screen
    # 403 Forbidden Meaning: “I know what you’re trying to do — but you are NOT allowed.” FE shows “Access denied”
    def get_queryset(self):
        if self.request.user.is_staff:
            return Suggestion.objects.all()
        return Suggestion.objects.none()
