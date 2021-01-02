from django.urls import path, include

urlpatterns = [
    path('', include('apps.core.urls')),
    path('inventory/', include('apps.inventory.urls')),
]
