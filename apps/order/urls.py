from django.urls import path

from apps.order.views.add_patient import AddPatientCreateAPIView, UserAddPatientListAPIView

app_name = 'order'

urlpatterns = [
    path('add-patient/create/', AddPatientCreateAPIView.as_view(), name='add-patient-create'),
    path('add-patient/list/', UserAddPatientListAPIView.as_view(), name='add-patient-create')
]