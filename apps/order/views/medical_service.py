from rest_framework.views import APIView

from apps.order.models import MedicalService
from apps.order.serializers.medical_service import OrderServiceListSerializer
from apps.utils.CustomResponse import CustomResponse


class OrderServiceListAPIView(APIView):
    serializer_class = OrderServiceListSerializer

    def get(self, request):
        obj = MedicalService.objects.filter(
            status=True
        ).order_by('-created_at')

        serializer = self.serializer_class(instance=obj, many=True)
        return CustomResponse.success_response(
            data=serializer.data
        )