# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
#
# from apps.notifications.thread import send_fcm_async
# from apps.order.models import Order, OrderStatusChoices
#
#
# @receiver(pre_save, sender=Order)
# def order_pre_save(sender, instance, **kwargs):
#     if not instance.pk:
#         return
#
#     old = Order.objects.filter(pk=instance.pk).only("status").first()
#     instance._old_status = old.status if old else None
#
#
# @receiver(post_save, sender=Order)
# def order_post_save(sender, instance, created, **kwargs):
#     if created:
#         return
#
#     if instance._old_status == instance.status:
#         return
#
#     if instance.status  in [OrderStatusChoices.WAITING, OrderStatusChoices.ON_THE_WAY]:
#         return
#
#     tokens = instance.user.devices.filter(is_active=True).values_list("token", flat=True)
#
#     title = body = None
#     if instance.status == OrderStatusChoices.ACCEPTED:
#         title = f"Buyurtma #{instance.order_id}"
#         body = f"Buyurtma qabul qilindi: {instance.doctor.fullname.title()}."
#
#     elif instance.status == OrderStatusChoices.ARRIVED:
#         title = f"Buyurtma #{instance.order_id}"
#         body = f"Shifokor yetib keldi."
#     elif instance.status == OrderStatusChoices.CANCELLED:
#         title = f"Buyurtma #{instance.order_id}"
#         body = f"Buyurtma bekor qilindi."
#     elif instance.status == OrderStatusChoices.FINISHED:
#         title = f"Buyurtma #{instance.order_id}"
#         body = f"Buyurtmangiz uchun rahmat"
#
#
#     for token in tokens:
#         send_fcm_async(
#             token=token,
#             title=title,
#             body=body,
#             extra_data={
#                 "order_id": str(instance.id),
#                 "status": instance.status
#             }
#         )
