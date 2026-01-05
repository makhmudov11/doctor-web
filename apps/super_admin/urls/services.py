from django.urls import path

from apps.banner.views import BannerListAPIView
from apps.service.views import ServiceListAPIView
from apps.super_admin.views.services import AdminBannerCreateAPIView, AdminServiceCreateAPIView, \
    AdminBannerRetrieveUpdateDestroyAPIView, AdminServicesRetrieveUpdateDestroyAPIView

app_name = 'home'

urlpatterns = [
    path('banner/create/', AdminBannerCreateAPIView.as_view(), name='admin-banner-create'),
    path('banner/list/', BannerListAPIView.as_view(), name='admin-banner-list'),
    path('banner/detail/<int:pk>/', AdminBannerRetrieveUpdateDestroyAPIView.as_view(), name='admin-banner-detail'),
    path('service/create/', AdminServiceCreateAPIView.as_view(), name='admin-service-create'),
    path('services/list/', ServiceListAPIView.as_view(), name='admin-service-list'),
    path('service/detail/<int:pk>/', AdminServicesRetrieveUpdateDestroyAPIView.as_view(), name='admin-service-detail'),
]
