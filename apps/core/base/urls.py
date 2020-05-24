from django.urls import path, include
from .views import *


app_name= 'base'

urlpatterns = [    
    path('', dashboard, name='dashboard'),
    path('sidebar/', sidebar, name='sidebar'),
]
