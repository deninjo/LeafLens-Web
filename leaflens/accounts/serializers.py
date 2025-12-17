from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    """
    defines how user registration data is validated and saved.
    """
    # Make password write-only so it is never returned in API responses
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User  # Uses Django's built-in User model
        fields = ["username", "email", "password"]  # Fields exposed to API

    def create(self, validated_data):
        # Called when serializer.save() is invoked
        # Creates a new User object using Django's create_user method
        # This handles password hashing automatically
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),  # email is optional
            password=validated_data["password"],
        )
        return user
