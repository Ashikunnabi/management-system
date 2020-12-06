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
    path('permission/add/', permission_add, name='permission_add'),
    path('permission/<int:id>/', permission_edit, name='permission_edit'),
    path('role/', role, name='role'),
    path('role/add/', role_add, name='role_add'),
    path('role/<int:id>/', role_edit, name='role_edit'),
    path('group/', group, name='group'),
    path('group/add/', group_add, name='group_add'),
    path('group/<int:id>/', group_edit, name='group_edit'),
    path('user/', user, name='user'),
    path('user/add/', user_add, name='user_add'),
    path('user/<int:id>/', user_edit, name='user_edit'),
    path('customer/', customer, name='customer'),
    path('feature/', feature, name='feature'),
    path('branch/', branch, name='branch'),
]
