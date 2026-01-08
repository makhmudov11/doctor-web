from django.urls import path

from apps.doctor_application.views import DoctorApplicationCreateAPIView, DoctorApplicationDetailAPIView, \
    SuccessDoctorApplicationAPIView

app_name = 'doctor_application'

urlpatterns = [
    path('create/', DoctorApplicationCreateAPIView.as_view(), name='doctor-create'),
    path('detail/<int:id>', DoctorApplicationDetailAPIView.as_view(), name='doctor-detail'),
    path('success/', SuccessDoctorApplicationAPIView.as_view(), name='doctor-app-success'),
]