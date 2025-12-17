from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Suggestion
from .serializers import SuggestionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# admin workflow
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# atomic transactions
from django.db import transaction



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



    # --------------------------------ADMIN WORKFLOW--------------------------------------#
    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """
        Admin approves a suggestion and merges it into Disease.metadata
        """
        suggestion = self.get_object()
        disease = suggestion.disease

        # ensure either everything succeeds or nothing is saved, wrap the approval logic in an atomic transaction
        with transaction.atomic():
            # Defensive: ensure metadata structure exists
            metadata = disease.metadata or {}
            metadata.setdefault('causes', [])
            metadata.setdefault('prevention', [])
            metadata.setdefault('treatment', [])

            # Prevent duplicates: check if suggestion already exists
            if suggestion.suggestion in metadata[suggestion.type]:
                return Response(
                    {"detail": "Duplicate suggestion. Already exists in disease metadata."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Append suggestion text
            metadata[suggestion.type].append(suggestion.suggestion)

            # Save disease metadata
            disease.metadata = metadata
            disease.save()

            # Update suggestion status
            suggestion.status = 'approved'
            suggestion.save()

        return Response(
            {"detail": "Suggestion approved and merged into disease metadata"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """
        Admin rejects a suggestion (no metadata changes)
        """
        suggestion = self.get_object()
        suggestion.status = 'rejected'
        suggestion.save()

        return Response(
            {"detail": "Suggestion rejected"},
            status=status.HTTP_200_OK
        )

