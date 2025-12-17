"""
URL configuration for leaflens project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView, # original view for login w/o last login write
    TokenRefreshView,
)
from accounts.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth endpoints
    # ex: POST /api/auth/login/
    path("api/auth/login/", CustomTokenObtainPairView.as_view()), # JWT login
    path("api/auth/refresh/", TokenRefreshView.as_view()),  # JWT token refresh
    path("api/auth/", include("accounts.urls")),  # User Registration endpoint

    # All APIs live under /api/
    path('api/', include('diseases.urls')),
    path('api/', include('predictions.urls')),
    path('api/', include('suggestions.urls'))
]
