from django.urls import path

from ..views.doctor_application import AdminDoctorApplicationListAPIView, AdminDoctorApplicationDetailAPIView, \
    AdminDoctorApplicationUpdateAPIView

app_name = 'doctor_application'

urlpatterns = [
    path('list/', AdminDoctorApplicationListAPIView.as_view(), name='admin-doctor-app-list'),
    path('detail/<int:id>', AdminDoctorApplicationDetailAPIView.as_view(), name='admin-doctor-app-detail'),
    path('update/<int:id>', AdminDoctorApplicationUpdateAPIView.as_view(), name='admin-doctor-app-update'),
]
