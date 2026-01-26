from decimal import Decimal

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.payment.payme.payme_link import PayComResponse
from apps.payment.serializers import PaymentProviderSerializer
from apps.transactions.models import TransactionProvider, UserUniqueBalanceID
from apps.utils.CustomResponse import CustomResponse


class PaymentFactory:
    RETURN_URL = "https://api.sinon.uz/"

    @staticmethod
    def get_gateway(payment_type: str, amount: int, balance_id: str = None):
        payment_type = payment_type.lower()
        if payment_type == TransactionProvider.PAYME:
            paycom = PayComResponse()
            return paycom.create_initialization(
                amount=amount * 100,
                balance_id=balance_id,
                return_url=PaymentFactory.RETURN_URL
            )
        raise ValueError("Mavjud bo'lmagan to'lov turi !")


class PaymentProviderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentProviderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider_name = serializer.validated_data.get('provider_name')
        amount = serializer.validated_data.get('amount')
        user_balance_obj = UserUniqueBalanceID.objects.filter(user=request.user).first()
        balance_id = user_balance_obj.balance_id
        url = PaymentFactory.get_gateway(payment_type=provider_name, amount=amount, balance_id=balance_id)
        return CustomResponse.success_response(
            data={"payment_url": url}
        )
