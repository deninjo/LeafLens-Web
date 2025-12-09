from rest_framework import serializers
from .models import Disease

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = [
            'id',
            'name',
            'scientific_name',
            'description',
            'metadata',
            'sample_image',
        ]

"""
Where this is used
GET /api/diseases/
GET /api/diseases/<id>/
POST /api/diseases/ (admin)
PUT/PATCH /api/diseases/<id>/ (admin)
Used by suggestions app when merging suggestions back into metadata
"""