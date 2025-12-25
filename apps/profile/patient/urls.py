from django.urls import path

from apps.profile.patient.views import PatientFollowListAPIView, PatientFollowUserCreateAPIView, \
    PatientUnfollowUserAPIView, PatientFollowCountAPIView

app_name = 'patient'

urlpatterns = [
    path('follow/list/', PatientFollowListAPIView.as_view(), name='patient-follow-list'),
    path('follow/count/', PatientFollowCountAPIView.as_view(), name='patient-follow-count'),
    path('follow/<int:profile_public_id>/', PatientFollowUserCreateAPIView.as_view(), name='patient-follow-user'),
    path('unfollow/<int:profile_public_id>/', PatientUnfollowUserAPIView.as_view(), name='patient-unfollow-user'),
]