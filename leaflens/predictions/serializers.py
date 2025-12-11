from rest_framework import serializers
from .models import Prediction

try:
    from diseases.serializers import DiseaseSerializer
except ImportError:
    # Fallback if direct import doesn't work
    from leaflens.diseases.serializers import DiseaseSerializer



class PredictionSerializer(serializers.ModelSerializer):
    predicted_disease = DiseaseSerializer(read_only=True)
    image_path = serializers.ImageField(read_only=True)
    explanation_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Prediction
        fields = [
            'id',
            'user',
            'image_path',
            'predicted_disease',
            'prediction_scores',
            'explanation_image',
            'created_at',
        ]

"""
Where this is used
POST /api/predict/ (after model inference)
GET /api/predictions/
GET /api/predictions/<id>/
user filtered analytics: /api/predictions/?user=123

Why make image fields read-only?
Because images are saved automatically by the prediction endpoint — not manually POSTed by the client.
"""


# for handling uploads in the Browsable API
class PredictionUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)