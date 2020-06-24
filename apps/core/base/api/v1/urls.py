from django.urls import path, include
from rest_framework import routers
from .viewsets import *


router = routers.DefaultRouter()
# router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # SMS API
    path('sms/', include([
        path('send/', send_sms, name='send_sms'),
        path('check_balance/', check_balance, name='check_sms_balance'),
        path('total_sent/', check_total_sms_sent, name='total_sent_sms'),
        path('expiry_date/', check_sms_expiry_date, name='sms_expiry_date'),
        path('rate/', get_sms_charge, name='sms_charge')    
    ])),
]
