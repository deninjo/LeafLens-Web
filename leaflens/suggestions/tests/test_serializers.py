from django.test import TestCase
from suggestions.serializers import SuggestionSerializer
from diseases.models import Disease
from django.contrib.auth.models import User

class SuggestionSerializerTest(TestCase):
    """
    Confirms your API will accept valid input
    Prevents silent serializer breakage later
    """

    # Create a test user before each test
    def setUp(self):
        self.user = User.objects.create_user(
            username="farmeruno",
            password="password123"
        )

        self.disease = Disease.objects.create(
            name="Common Rust",
            metadata={}
        )

    # validate incoming input
    def test_serializer_valid_data(self):
        data = {
            "disease": self.disease.id,
            "user": self.user.id,
            "type": "treatment",
            "suggestion": "Use fungicide"
        }

        serializer = SuggestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
