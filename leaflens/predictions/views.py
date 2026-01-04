from django.shortcuts import render

# predict
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework.parsers import MultiPartParser, FormParser

from .models import Prediction
from .serializers import PredictionSerializer
from rest_framework.exceptions import ValidationError
from .serializers import PredictionUploadSerializer
from diseases.models import Disease


from ml.utils import is_maize_clip, run_tflite_inference

from .throttles import PredictAnonThrottle, PredictUserThrottle

# retrieve predictions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Prediction
from .serializers import PredictionSerializer

# filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import renderers
from .filters import PredictionFilter


# Create your views here.

# CreateAPIView automatically renders a Browsable API form for file uploads:
class PredictAPIView(CreateAPIView):
    """
        Handles POST requests with an image and performs
        inference x prediction
    """
    # custom throttles for api rate limiting
    throttle_classes = [PredictAnonThrottle, PredictUserThrottle]

    # Handles file uploads (multipart/form-data) and regular form fields
    parser_classes = [MultiPartParser, FormParser]

    # Serializer to validate uploaded image
    serializer_class = PredictionUploadSerializer
    permission_classes = []  # allow anonymous for now

    # overriding get()
    def get(self, request, *args, **kwargs):
        """Overiding GET to display a message to the user to Use POST to upload image"""
        return Response({"detail": "Use POST to upload image"}, status=200)


    def perform_create(self, serializer):
        # Extract uploaded image from validated serializer data
        uploaded_image = serializer.validated_data["image"]

        # Save the uploaded image temporarily in the media folder
        saved_path = default_storage.save(f"predictions/{uploaded_image.name}",
                                          ContentFile(uploaded_image.read()))

        # Step 1: CLIP prefilter
        if not is_maize_clip(default_storage.path(saved_path)):
            # Save CLIP-rejected images (Recommended for ML systems) best ML engineering practice.
            prediction = Prediction.objects.create(
                user=self.request.user if self.request.user.is_authenticated else None,
                image_path=saved_path,
                predicted_disease=None,  # null
                prediction_scores={"is_maize": False},
                explanation_image=None
            )

            self.instance = prediction
            return  # stop here, do NOT run TFLite

        # Step 2: Run TFLite disease classifier
        predicted_label, scores = run_tflite_inference(default_storage.path(saved_path))

        # Step 3: Try to link predicted label to a Disease object in DB if exists
        disease_obj = Disease.objects.filter(name__iexact=predicted_label).first()

        # Step 4: Create the Prediction record in database
        prediction = Prediction.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            image_path=saved_path,
            predicted_disease=disease_obj,
            prediction_scores=scores,
        )

        # Save the instance for later serialization in create()
        self.instance = prediction  # Save for serializer


    def create(self, request, *args, **kwargs):
        """
        Override to return PredictionSerializer output
        returns serialized JSON with prediction info.
        """
        #  Deserialize input
        serializer = self.get_serializer(data=request.data)

        # Validate (raises 400 if image not submitted)
        serializer.is_valid(raise_exception=True)

        # Run perform_create (image saved, ML inference, Prediction record created)
        self.perform_create(serializer)

        # Serialize full Prediction object for API response
        response_serializer = PredictionSerializer(self.instance)

        # Return JSON with prediction result
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)





# the "CRUD part" of predictions
class PredictionViewSet(viewsets.ModelViewSet):
    """
    Handles GET (list/retrieve) and DELETE for Prediction objects.
    Filters results by authenticated user.
    """
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

    # Enable filtering, searching, ordering
    renderer_classes = [renderers.JSONRenderer, renderers.BrowsableAPIRenderer]  # browsable API UI/returns JSON
    filterset_class = PredictionFilter

    search_fields = [
        'predicted_disease__name',
    ]

    ordering_fields = ['created_at', 'id']
    ordering = ['-created_at']


    def get_queryset(self):
        user = self.request.user
        # If user is authenticated → return their predictions
        if user.is_authenticated:
            return Prediction.objects.filter(user=user)

        # If anonymous → return none
        return Prediction.objects.none()


