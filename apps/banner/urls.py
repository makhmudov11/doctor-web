from django.urls import path

from apps.banner.views import BannerListAPIView, BannerDetailAPIView

app_name = 'banner'

urlpatterns = [
    path('list/', BannerListAPIView.as_view(), name='banner-list'),
    path('detail/<int:banner_id>', BannerDetailAPIView.as_view(), name='banner-detail')
]