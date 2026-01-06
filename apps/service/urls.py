from django.urls import path

from apps.history.views.social_network import SocialNetworkListAPIView, SocialNetworkDetailAPIView
from apps.service.models import SocialNetwork
from apps.service.views import ServiceListAPIView, ServiceDetailAPIView

app_name = 'service'

urlpatterns = [
    path('list/', ServiceListAPIView.as_view(), name='service-list'),
    path('detail/<int:service_id>', ServiceDetailAPIView.as_view(), name='service-detail'),
    path('social_network/list', SocialNetworkListAPIView.as_view(), name='social_network-list'),
    path('social_network/detail/<int:social_id>', SocialNetworkDetailAPIView.as_view(), name='social_network-detail'),
]