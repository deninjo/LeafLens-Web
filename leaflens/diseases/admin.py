from django.contrib import admin

from .models import Disease

# Register your models here.
@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('name', 'scientific_name', 'description', 'metadata', 'sample_image')
