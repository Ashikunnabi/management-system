from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.core.rbac.api.v1.urls')),
]

