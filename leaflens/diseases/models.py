from django.db import models

# Create your models here.
class Disease(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict)   # {"causes": [], "prevention": [], "treatment": []}
    sample_image = models.URLField(null=True, blank=True) #  Django validates that the value is a valid URL

    def __str__(self):
        return self.name
