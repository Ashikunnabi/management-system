from django.urls import path, include
from .views import *


app_name= 'base'

urlpatterns = [ 
    path('api/', include('apps.core.base.api.urls')),   
    path('', dashboard, name='dashboard'),
    path('sidebar/', sidebar, name='sidebar'),
]
