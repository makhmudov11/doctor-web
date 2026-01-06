from django.urls import path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.permissions import AllowAny

SPECTACULAR_URL = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui', ),
    path(
        'api/schema/swagger/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
            permission_classes=[AllowAny]
        ),
        name='swagger-ui'
    ),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
