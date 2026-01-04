from django.urls import path
from ..views.profile import AdminDoctorProfileListAPIView, AdminDoctorProfileCreateAPIView, AdminDoctorProfileRetrieveUpdateDestroyAPIView, AdminPatientProfileListAPIView, AdminPatientProfileCreateAPIView, AdminPatientProfileRetrieveUpdateDestroyAPIView
app_name = 'profile'

urlpatterns = [
    path('doctor/list/', AdminDoctorProfileListAPIView.as_view(), name='admin-doctor-profile-list'),
    path('doctor/create/', AdminDoctorProfileCreateAPIView.as_view(), name='admin-doctor-profile-create'),
    path('doctor/detail/<int:pk>/', AdminDoctorProfileRetrieveUpdateDestroyAPIView.as_view(), name='admin-doctor-profile-detail'),
    
    path('patient/list/', AdminPatientProfileListAPIView.as_view(), name='admin-patient-profile-list'),
    path('patient/create/', AdminPatientProfileCreateAPIView.as_view(), name='admin-patient-profile-create'),
    path('patient/detail/<int:pk>/', AdminPatientProfileRetrieveUpdateDestroyAPIView.as_view(), name='admin-patient-profile-detail'),
]