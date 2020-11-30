# from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('apps.urls')),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)

handler400 = 'apps.core.base.views.handler400'
handler403 = 'apps.core.base.views.handler403'
handler404 = 'apps.core.base.views.handler404'
handler500 = 'apps.core.base.views.handler500'
