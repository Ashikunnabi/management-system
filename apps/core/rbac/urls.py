from django.urls import path, include
from .views import *


app_name= 'rbac'

urlpatterns = [    
    path('api/', include('apps.core.rbac.api.urls')),
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('reset/', reset, name='reset'),
    path('change-password/', change_password, name='change_password'),
    path('permission/', permission, name='permission'),
    path('role/', role, name='role'),
    path('user/', user, name='user'),
    path('user/add/', user_add, name='user_add'),
    path('customer/', customer, name='customer'),
    path('feature/', feature, name='feature'),
]
