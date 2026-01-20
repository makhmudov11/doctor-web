from django.urls import path
from ..views.medical_service import AdminMedicalServiceListAPIVew, AdminMedicalServiceCreateAPIView

app_name = 'medical-service'


urlpatterns = [
    path('service/list/', AdminMedicalServiceListAPIVew.as_view(), name='admin-medical-service'),
    path('service/create/', AdminMedicalServiceCreateAPIView.as_view(), name='admin-medical-service')
]