from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .views import api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('auth/', include('auth_app.urls')),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
