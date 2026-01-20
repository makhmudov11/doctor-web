from django.urls import path

from apps.transactions.views import UserBalanceAPIView

app_name = 'transactions'

urlpatterns = [
    # path('provider/', UserChooseProviderAPIView.as_view(), name='provider-name')
    path('user/balance/', UserBalanceAPIView.as_view(), name='user-balance')
]
