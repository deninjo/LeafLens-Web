from django.urls import path, include
from .views import PredictionViewSet, PredictAPIView

# view set for drf
from rest_framework.routers import DefaultRouter

# Create router
# Router automatically generates all the necessary URLs for each CRUD action:
router = DefaultRouter()
router.register(r'predictions', PredictionViewSet, basename='predictions')


# Define URL patterns
urlpatterns = [
    # ex: api/predict/ → PredictAPIView (ML + save prediction)
    path('predict/', PredictAPIView.as_view(), name='predict'),

    # router handles all CRUD URLs
    # ex: /api/predictions/ → PredictionViewSet (list, retrieve, delete)
    # GET list → /api/predictions/
    # GET single → /api/predictions/<id>/
    # DELETE → /api/predictions/<id>/
    path('', include(router.urls)),
]