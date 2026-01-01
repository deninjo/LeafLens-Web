from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class RegisterView(APIView):
    """
    API endpoint for user registration.
    Default behavior: creates farmer users (is_staff=False)
    """
    permission_classes = [AllowAny]  # No authentication required

    def post(self, request):
        # Initialize serializer with the POSTed data
        serializer = RegisterSerializer(data=request.data)

        # Validate input data (checks username uniqueness, email format, password)
        if serializer.is_valid():
            # Save the new User object
            serializer.save()
            return Response(
                {"detail": "User registered successfully"},
                status=status.HTTP_201_CREATED,  # HTTP 201 = created
            )

        # If validation fails, return errors with HTTP 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LogoutView(APIView):
    """
    Logs out a user by blacklisting their refresh token.
    """
    permission_classes = [IsAuthenticated]  # Only logged-in users can log out

    def post(self, request):
        """
        Accepts a refresh token in the request body and blacklists it.
        After blacklisting, that refresh token cannot be used again.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Add this refresh token to the blacklist table
            return Response({"detail": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)




class CustomTokenObtainPairView(TokenObtainPairView):
    """ensures that whenever a user logs in through JWT, last_login is updated."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Get user from serializer's validated data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user

            # Update last_login
            update_last_login(None, user)
        return response
