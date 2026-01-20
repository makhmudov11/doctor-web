from django.urls import path

from apps.order.views.add_patient import AddPatientCreateAPIView, UserAddPatientListAPIView, \
    UserAddPatientDetailAPIView
from apps.order.views.medical_service import OrderServiceListAPIView
from apps.order.views.orders import OrderCreateAPIView, GetOrderDetailAPIView, UserOrderAndBalanceHistoryListAPIView

app_name = 'order'

urlpatterns = [
    path('add-patient/create/', AddPatientCreateAPIView.as_view(), name='add-patient-create'),
    path('add-patient/list/', UserAddPatientListAPIView.as_view(), name='add-patient-create'),
    path('add-patient/detail/<int:patient_id>', UserAddPatientDetailAPIView.as_view(), name='add-patient-detail'),
    path('services/list', OrderServiceListAPIView.as_view(), name='order-services'),
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('detail/<order_id>', GetOrderDetailAPIView.as_view(), name='order-detail'),
    path('balance/history/', UserOrderAndBalanceHistoryListAPIView.as_view(), name='order-balance-history-list'),
]
