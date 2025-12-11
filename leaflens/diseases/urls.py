from django.urls import path, include
from .views import DiseaseViewSet

# view set for drf
from rest_framework.routers import DefaultRouter

# Create router
# Router automatically generates all the necessary URLs for each CRUD action:
router = DefaultRouter()
router.register(r'diseases', DiseaseViewSet, basename='disease')


# Define URL patterns
urlpatterns = [
    # router handles all CRUD URLs
    # ex: api/diseases/
    # ex: api/diseases/<id>/
    path('', include(router.urls)),
]