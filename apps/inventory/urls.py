from django.urls import path, include
from .views import category


urlpatterns = [
    path('api/', include('apps.inventory.api.urls')),
    path('category/', category, name='category')
]
