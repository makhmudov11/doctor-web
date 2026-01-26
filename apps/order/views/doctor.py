from rest_framework.views import APIView

from apps.order.models import Order, OrderStatusChoices
from apps.profile.models import DoctorProfile
from apps.profile.permission import IsDoctor
from apps.utils.CustomResponse import CustomResponse
from django.utils.translation import gettext_lazy as _

from apps.utils.role_validate import RoleValidate


class DoctorAcceptedOrder(APIView):
    permission_classes = [IsDoctor]


    def get(self, request, order_id):
        if not order_id:
            return CustomResponse.error_response(
                message=_("Buyurtma raqami kelishi shart")
            )
        try:
            order = Order.objects.get(
                order_id=order_id,
                doctor=RoleValidate.get_profile_user(request),
                status=OrderStatusChoices.WAITING
            )
        except Order.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Buyurtma topilmadi")
            )
        order.status = OrderStatusChoices.ACCEPTED
        order.save(update_fields=['status'])
