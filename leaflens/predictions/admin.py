from django.contrib import admin
from .models import Prediction

# Register your models here.
@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('user', 'image_path', 'predicted_disease', 'prediction_scores', 'explanation_image', 'created_at')
