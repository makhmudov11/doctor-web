from django.urls import path
from ..views.profile import AdminDoctorProfileListAPIView, AdminPatientProfileListAPIView, \
    AdminPatientProfileRetrieveAPIView, AdminDoctorProfileRetrieveAPIView

app_name = 'profile'

urlpatterns = [
    path('doctor/list/', AdminDoctorProfileListAPIView.as_view(), name='admin-doctor-profile-list'),
    path('doctor/detail/<int:public_id>/', AdminDoctorProfileRetrieveAPIView.as_view(),
         name='admin-doctor-profile-detail'),

    path('patient/list/', AdminPatientProfileListAPIView.as_view(), name='admin-patient-profile-list'),
    path('patient/detail/<int:public_id>/', AdminPatientProfileRetrieveAPIView.as_view(), name='admin-patient-profile-detail'),
]
