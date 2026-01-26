from django.urls import path, include

from apps.payment.payme.views import PayComAPIView
from apps.payment.view import PaymentProviderAPIView

app_name = 'payment'

urlpatterns = [
    # path('payme/', PayComAPIView.as_view(), name='payme'),
    # path('', PaymentProviderAPIView.as_view(), name='payment_provider')
]