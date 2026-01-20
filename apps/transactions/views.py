from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.transactions.models import UserUniqueBalanceID
from apps.utils.CustomResponse import CustomResponse
from django.utils.translation import gettext_lazy as _


class UserBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            balance_obj = UserUniqueBalanceID.objects.get(user=request.user)
        except UserUniqueBalanceID.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Foydalanuvchi hisobi topilmadi")
            )

        return CustomResponse.success_response(
            data={"balance" : balance_obj.balance}
        )
