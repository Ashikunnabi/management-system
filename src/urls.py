from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
]

handler400 = 'apps.core.base.views.handler400'
handler403 = 'apps.core.base.views.handler403'
handler404 = 'apps.core.base.views.handler404'
handler500 = 'apps.core.base.views.handler500'