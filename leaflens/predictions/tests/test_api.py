# predictions/tests/test_api.py

import io
from unittest.mock import patch
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from predictions.models import Prediction
from diseases.models import Disease


class PredictionAPITest(APITestCase):
    """
    Tests prediction endpoints end-to-end:
    - Authenticated prediction
    - Anonymous prediction
    - Authenticated user prediction history
    """

    # Creates a test user and fake diseases in the database.
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="farmeruno",
            password="password123"
        )

        # Create fake diseases in DB for serializer mapping
        self.blight = Disease.objects.create(name="Blight")
        self.rust = Disease.objects.create(name="Common Rust")
        self.gray = Disease.objects.create(name="Gray Leaf Spot")
        self.healthy = Disease.objects.create(name="Healthy")

    # Helper to log in and attach JWT token to client
    def authenticate(self):
        '''Every request made after this includes the token, so DRF sees the user as authenticated.'''
        response = self.client.post(
            "/api/auth/login/",
            {"username": "farmeruno", "password": "password123"}
        )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Helper to create a valid fake image
    def create_fake_image(self):
        image_file = io.BytesIO()
        image = Image.new("RGB", (10, 10), color=(255, 0, 0))  # small red image
        image.save(image_file, format="JPEG")
        image_file.seek(0)
        return SimpleUploadedFile(
            name="test.jpg",
            content=image_file.read(),
            content_type="image/jpeg"
        )

    # patch replaces the real functions temporarily
    @patch("predictions.views.is_maize_clip", return_value=True)
    @patch("predictions.views.run_tflite_inference")
    def test_authenticated_user_can_predict(self, mock_inference, mock_is_maize):
        """
        Tests that an authenticated user can POST an image and get
        a valid prediction saved in the database.
        """
        self.authenticate()

        # Mock ML output
        mock_inference.return_value = (
            "Common Rust",  # predicted label
            {
                "Blight": 0.006064,
                "Healthy": 0.0000001,
                "Common Rust": 0.917859,
                "Gray Leaf Spot": 0.076076
            }
        )

        fake_image = self.create_fake_image()

        response = self.client.post(
            "/api/predict/",
            {"image": fake_image},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("predicted_disease", response.data)
        self.assertEqual(response.data["predicted_disease"]["name"], "Common Rust")
        self.assertIn("prediction_scores", response.data)
        self.assertEqual(response.data["prediction_scores"]["Common Rust"], 0.917859)

    # patch replaces the real functions temporarily
    @patch("predictions.views.is_maize_clip", return_value=True)
    @patch("predictions.views.run_tflite_inference")
    def test_anonymous_user_can_predict(self, mock_inference, mock_is_maize):
        """
        Tests that an anonymous user can POST an image and get
        a prediction (user=None in DB).
        """
        mock_inference.return_value = (
            "Blight",
            {"Blight": 0.8, "Healthy": 0.05, "Common Rust": 0.1, "Gray Leaf Spot": 0.05}
        )

        fake_image = self.create_fake_image()

        response = self.client.post(
            "/api/predict/",
            {"image": fake_image},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["predicted_disease"]["name"], "Blight")
        self.assertIsNone(response.data["user"])  # user should be None for anonymous

    # patch replaces the real functions temporarily
    @patch("predictions.views.is_maize_clip", return_value=True)
    @patch("predictions.views.run_tflite_inference")
    def test_authenticated_user_prediction_history(self, mock_inference, mock_is_maize):
        """
        Authenticated user can retrieve their own predictions
        """
        self.authenticate()

        # Create 2 predictions
        mock_inference.return_value = ("Gray Leaf Spot", {"Gray Leaf Spot": 1.0})
        fake_image1 = self.create_fake_image()
        fake_image2 = self.create_fake_image()

        self.client.post("/api/predict/", {"image": fake_image1}, format="multipart")
        self.client.post("/api/predict/", {"image": fake_image2}, format="multipart")

        # Retrieve user's predictions
        response = self.client.get("/api/predictions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # two predictions returned
        for pred in response.data:
            self.assertEqual(pred["user"], self.user.id)  # all belong to logged-in user
