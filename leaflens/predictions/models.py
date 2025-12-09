from django.db import models
from django.contrib.auth.models import User



class Prediction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    image_path = models.ImageField(upload_to='predictions/') # stores only the path

    predicted_disease = models.ForeignKey(
        'diseases.Disease',  # Use string reference with app_name.ModelName
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='predictions',
    )

    prediction_scores = models.JSONField()
    # e.g. {"blight":0.82,"rust":0.12,"healthy":0.06}
    # Or CLIP filter: {"is_maize": false}

    explanation_image = models.ImageField(upload_to='xai/', null=True, blank=True) # stores only the path

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id} for {self.user}"
