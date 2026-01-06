from django.urls import path

from apps.history.views.address import PatientAddressAPIView, AddressCreateAPIView, AddressDeleteAPIView, \
    AddressDetailAPIView

app_name = 'history'

urlpatterns = [
    path('address/<int:patient_public_id>/list/', PatientAddressAPIView.as_view(), name='patient-address-list', ),
    path('address/create/', AddressCreateAPIView.as_view(), name='patient-address-create'),
    path('address/delete/<int:address_id>', AddressDeleteAPIView.as_view(), name='patient-address-delete'),
    path('address/detail/<int:address_id>', AddressDetailAPIView.as_view(), name='patient-address-detail'),
]