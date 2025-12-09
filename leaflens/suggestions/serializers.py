from rest_framework import serializers
from .models import Suggestion

class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = [
            'id',
            'disease',
            'user',
            'type',
            'suggestion',
            'status',
            'created_at',
        ]
        # client (frontend or API consumer) is NOT allowed to set or modify
        # these fields when creating or updating a Suggestion.
        read_only_fields = ['status', 'created_at']


'''
Where this is used
POST /api/suggestions/ (farmer submits)
GET /api/suggestions/?status=pending (admin dashboard)
PATCH /api/suggestions/<id>/approve (admin)
PATCH /api/suggestions/<id>/reject (admin)
'''