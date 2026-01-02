from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class JWTAuthTest(APITestCase):
    """
    Proves:
    JWT login works
    Tokens are returned
    Protected endpoints reject anonymous users
    """

    # Create a test user before each test
    def setUp(self):
        self.user = User.objects.create_user(
            username="farmeruno",
            password="password123"
        )

    # Test successful login returns access and refresh tokens
    def test_login_returns_tokens(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "farmeruno",
                "password": "password123"
            }
        )
        # Verify successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that both tokens are present in response
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


# Test that protected endpoints reject unauthenticated requests
    def test_protected_endpoint_requires_auth(self):
        response = self.client.post("/api/suggestions/",
    {
            "disease": 2,
            "user": self.user.id,
            "type": "treatment",
            "suggestion": "Use fungicide"
        })

        # Verify unauthorized access is blocked
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
