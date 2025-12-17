"""
Limit how many API requests a client can make per minute
stricter rules for /predict/.
"""

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class PredictAnonThrottle(AnonRateThrottle):
    scope = "predict_anon"

class PredictUserThrottle(UserRateThrottle):
    scope = "predict_user"
