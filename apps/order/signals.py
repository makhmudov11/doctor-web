from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.order.models import Order
from apps.order.serializers.orders import OrderDetailFullSerializer

@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    print("🔥 NANO FIRED", instance.id, instance.status)
    if instance.id:
        print("🔥 SIGNAL FIRED", instance.id, instance.status)
        instance._old_status = Order.objects.get(id=instance.id).status


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        return

    if getattr(instance, "_old_status", None) == instance.status:
        return

    channel_layer = get_channel_layer()
    group_name = f"order_{instance.order_id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "order_update",
            "data": {
                "order_id" : instance.order_id,
                "name" : instance.patient.user.full_name or 'NANO',
                "status": instance.status
            }
        }
    )
