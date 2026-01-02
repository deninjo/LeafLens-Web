from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from diseases.models import Disease
from suggestions.models import Suggestion
from rest_framework import status

class SuggestionAPITest(APITestCase):
    """Test suggestion submission and approval workflows"""

    def setUp(self):
        """Set up test data: admin user, regular farmer user, and sample disease"""
        # Create admin user with staff privileges
        self.admin = User.objects.create_user(
            username="admin",
            password="adminpass",
            is_staff=True
        )

        # Create regular farmer user
        self.farmer = User.objects.create_user(
            username="farmer",
            password="farmerpass"
        )

        # Create a sample disease for testing
        self.disease = Disease.objects.create(
            name="Blight",
            metadata={"causes": [], "prevention": [], "treatment": []}
        )

    def authenticate(self, user):
        """Helper method to authenticate a user and set JWT token in request headers"""
        # Login to get JWT token
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": user.username,
                "password": "adminpass" if user.is_staff else "farmerpass"
            }
        )
        token = response.data["access"]
        # Set Authorization header with Bearer token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_farmer_can_submit_suggestion(self):
        """Test that a farmer can successfully submit a new suggestion"""
        # Authenticate as farmer
        self.authenticate(self.farmer)

        # Submit suggestion for disease prevention
        response = self.client.post(
            "/api/suggestions/",
            {
                "disease": self.disease.id,
                "type": "prevention",
                "suggestion": "Crop rotation"
            },
            format="json"
        )

        # Verify suggestion was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_approve_suggestion(self):
        """Test that admin can approve a submitted suggestion"""
        # Create a suggestion submitted by farmer
        suggestion = Suggestion.objects.create(
            disease=self.disease,
            user=self.farmer,
            type="prevention",
            suggestion="Crop rotation"
        )

        # Authenticate as admin
        self.authenticate(self.admin)

        # Approve the suggestion
        response = self.client.patch(
            f"/api/suggestions/{suggestion.id}/approve/"
        )

        # Verify approval was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)