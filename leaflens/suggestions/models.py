from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Suggestion(models.Model):
    disease = models.ForeignKey(
        'diseases.Disease',  # Use string reference with app_name.ModelName
        related_name="suggestions",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        related_name="suggestions",
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=20,
        choices=[
            ('cause', 'Cause'),
            ('prevention', 'Prevention'),
            ('treatment', 'Treatment'),
        ]
    )

    suggestion = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for {self.disease.name}"
