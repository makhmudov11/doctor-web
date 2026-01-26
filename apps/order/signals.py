from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.order.models import Order
from apps.order.serializers.orders import OrderDetailFullSerializer


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    if instance.id:
        try:
            old_order = Order.objects.get(id=instance.id)
            instance._old_status = old_order.status
            instance._old_doctor = old_order.doctor
        except Order.DoesNotExist:
            pass

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:

        # Bemor uchun yangilanish yuboramiz (waiting holatida)
        channel_layer = get_channel_layer()
        serializer_data = OrderDetailFullSerializer(instance).data
        group_name = f"order_{instance.order_id}"

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "order_update",  # Bemor uchun
                "data": serializer_data
            }
        )

        # Doktor uchun yangilanish yuborish (zayafka holatida)
        if instance.doctor:
            doctor_group_name = f"doctor_{instance.doctor.id}"
            async_to_sync(channel_layer.group_send)(
                doctor_group_name,
                {
                    "type": "order_doctor_update",  # Doktor uchun
                    "data": {
                        **serializer_data,
                        "for_doctor": True,
                        "event_type": "zayafka",  # Zayafka holati
                        "status": "waiting",  # Buyurtma hali qabul qilinmagan
                        "order_id": instance.order_id,
                    }
                }
            )
        return

    # Status o'zgargan bo'lsa, yangilanish yuboriladi
    if getattr(instance, "_old_status", None) == instance.status:
        return

    channel_layer = get_channel_layer()
    serializer_data = OrderDetailFullSerializer(instance).data
    group_name = f"order_{instance.order_id}"

    # Bemor uchun yangilanish yuborish
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "order_update",  # Bemor uchun
            "data": serializer_data
        }
    )

    # Doktor uchun yangilanish yuborish
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "order_doctor_update",  # Doktor uchun
            "data": {
                **serializer_data,
                "for_doctor": True,
                "event_type": "status_changed",  # Status o'zgarganda
                "old_status": getattr(instance, "_old_status", None),
                "new_status": instance.status
            }
        }
    )
