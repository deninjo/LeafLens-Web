from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuggestionViewSet

# Create router
# Router automatically generates all the necessary URLs for each CRUD action:
router = DefaultRouter()
router.register(r'suggestions', SuggestionViewSet, basename='suggestions')


# Define URL patterns
urlpatterns = [

# router handles all CRUD URLs
    # ex: api/suggestions/
    # ex: api/suggestions/<id>/
    path('', include(router.urls)),
]
