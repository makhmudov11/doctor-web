from itertools import chain

from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.history.models import Address
from apps.order.models import Order, AddPatient, PaymentTypeChoice, OrderDetailImage, OrderDetail, MedicalService, \
    OrderStatusChoices
from apps.order.serializers.orders import OrderCreateSerializer, OrderDetailFullSerializer, MedicalServiceSerializer, \
    OrderHistoryAndBalanceSerializer, UserHistoryResponseSerializer
from apps.profile.models import DoctorProfile
from apps.profile.permission import IsPatient
from apps.transactions.models import UserUniqueBalanceID, Transactions, TransactionChoices
from apps.transactions.serializers import UserTransactionHistorySerializer
from apps.utils.CustomResponse import CustomResponse
from apps.utils.role_validate import RoleValidate
from django.utils.translation import gettext_lazy as _


@extend_schema(
    responses={201: OrderDetailFullSerializer}
)
class OrderCreateAPIView(CreateAPIView):
    """
    doctor uchun oddiy id emas proile public id
    """
    permission_classes = [IsPatient]
    serializer_class = OrderCreateSerializer
    queryset = orders = Order.objects.select_related(
        'patient', 'add_patient', 'doctor', 'address'
    ).prefetch_related(
        'order_images',
        'order_details'
    )

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        patient_orders = Order.objects.filter(patient=RoleValidate.get_profile_user(request)).order_by(
            '-created_at').first()
        if patient_orders.status not in [OrderStatusChoices.CANCELLED, OrderStatusChoices.FINISHED]:
            return CustomResponse.error_response(
                message=_("Sizda tugallanmagan buyurtma mavjud")
            )
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        try:
            add_patient = AddPatient.objects.get(
                id=serializer.validated_data['add_patient']
            )
            doctor = DoctorProfile.objects.get(
                id=serializer.validated_data['doctor'].id,
                status=True
            )
            if doctor.user == request.user:
                return CustomResponse.error_response(
                    message=_("O'z o'zini chaqirish mumkin emas")
                )
            address = Address.objects.get(
                id=serializer.validated_data['address_id'],
                patient=RoleValidate.get_profile_user(request)
            )
        except AddPatient.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Bemor id topilmadi")
            )
        except DoctorProfile.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Shifokor public id topilmadi")
            )
        except Address.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Manzil topilmadi")
            )

        payment_type = serializer.validated_data.get('payment_type')
        services = serializer.validated_data.get('services', [])

        summa = 0
        service_obj = None

        try:
            with transaction.atomic():
                if services:
                    for service in services:
                        service_obj = MedicalService.objects.filter(id=service['id'], status=True).first()
                        if not service_obj:
                            return CustomResponse.error_response(
                                message=_("Ushbu service topilmadi"),
                                data=MedicalServiceSerializer(instance=service).data
                            )
                        summa += service['count'] * service_obj.price
                summa += int(doctor.service_fee)
                if int(summa) != serializer.validated_data['summa']:
                    return CustomResponse.error_response(
                        message=_("Summa noto'g'ri hisoblangan"),
                        data={"summa": serializer.validated_data['summa']}
                    )
                order_create = Order(
                    patient=RoleValidate.get_profile_user(request),
                    add_patient=add_patient,
                    doctor=doctor,
                    address=address,
                    summa=summa
                )

                balance_id_obj = None
                if payment_type == PaymentTypeChoice.BALANS:
                    try:
                        balance_id_obj = request.user.user_balance_id
                    except UserUniqueBalanceID.DoesNotExist:
                        raise Exception(_("Userga tegishli hisob raqami topilmadi"))

                    if balance_id_obj.balance < summa:
                        raise Exception(_("Foydalanuvchi hisobida mablag' yetarli emas"))

                    balance_id_obj.balance -= summa
                    balance_id_obj.save()
                    order_create.payment_type = PaymentTypeChoice.BALANS

                order_create.save()

                images_objs = [
                    OrderDetailImage(order=order_create, prescription=img)
                    for img in serializer.validated_data.get('prescription', [])
                ]
                OrderDetailImage.objects.bulk_create(images_objs)

                services = OrderDetail.objects.create(order=order_create, medical_service=services)

                response_serializer = OrderDetailFullSerializer(order_create,
                                                                context={"request": request})
                return CustomResponse.success_response(
                    message=_("Buyurtma muvaffaqiyatli yaratildi"),
                    data=response_serializer.data,
                    code=status.HTTP_201_CREATED
                )
        except Exception as e:
            return CustomResponse.error_response(
                message=_(f"Buyurtma saqlashda xatolik: {str(e)} ")
            )


class GetOrderDetailAPIView(APIView):
    serializer_class = OrderDetailFullSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        if not order_id:
            return CustomResponse.error_response(
                message=_("Buyurtma raqami topilmadi")
            )
        try:
            order_obj = Order.objects.get(
                order_id=order_id,
                patient=RoleValidate.get_profile_user(request)
            )
        except Order.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Buyurtma topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(order_obj)
        return CustomResponse.success_response(
            data=serializer.data
        )

class UserOrderAndBalanceHistoryListAPIView(APIView):
    """

    """
    # permission_classes = [IsAuthenticated]
    serializer_class = UserHistoryResponseSerializer

    def get(self, request):
        profile = RoleValidate.get_profile_user(request)

        orders = Order.objects.filter(
            patient=profile,
        ).exclude(
            status=OrderStatusChoices.CANCELLED
        )

        balance_history = Transactions.objects.filter(
            balance_id__user=profile.user,
            status=TransactionChoices.SUCCESS
        )
        print(balance_history)

        order_data = OrderHistoryAndBalanceSerializer(
            orders, many=True
        ).data

        balance_data = UserTransactionHistorySerializer(
            balance_history, many=True
        ).data

        history = list(chain(order_data, balance_data))

        history.sort(key=lambda x: x['created_at'], reverse=True)

        return CustomResponse.success_response(
            data=history
        )

