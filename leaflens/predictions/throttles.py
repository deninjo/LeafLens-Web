"""
Limit how many API requests a client can make per minute
stricter rules for /predict/.
"""

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class PredictAnonThrottle(AnonRateThrottle):
    '''throttling is counted per IP address 4 anonymous users'''
    scope = "predict_anon"

class PredictUserThrottle(UserRateThrottle):
    '''throttling is counted per user account (user_id)'''
    scope = "predict_user"
