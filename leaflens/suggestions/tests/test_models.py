from django.test import TestCase
from django.contrib.auth.models import User
from diseases.models import Disease
from suggestions.models import Suggestion

class SuggestionModelTest(TestCase):
    """
    Tests basic behavior of the Suggestion model
    This test proves:
    The model’s default behavior works
    New suggestions are pending by default
    Database schema behaves as expected
    """

    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username="farmeruno",
            password="password123"
        )

        # Create disease
        self.disease = Disease.objects.create(
            name="Common Rust",
            metadata={
                "causes": [],
                "prevention": [],
                "treatment": []
            }
        )

    def test_suggestion_defaults_to_pending(self):
        suggestion = Suggestion.objects.create(
            disease=self.disease,
            user=self.user,
            type="prevention",
            suggestion="Crop rotation"
        )

        self.assertEqual(suggestion.status, "pending")
