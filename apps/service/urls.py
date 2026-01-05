from django.urls import path

from apps.service.views import ServiceListAPIView, ServiceDetailAPIView

app_name = 'service'

urlpatterns = [
    path('list/', ServiceListAPIView.as_view(), name='service-list'),
    path('detail/<int:service_id>', ServiceDetailAPIView.as_view(), name='service-detail')
]