from django.urls import path
from .views import RegisterView, LogoutView

# Define URL patterns
urlpatterns = [
    # ex: POST /api/auth/register/
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view())
]
