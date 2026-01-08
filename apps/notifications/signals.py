# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order
# from yourapp.notifications import Notifications
#
# @receiver(post_save, sender=Order)
# def send_order_notification(sender, instance, created, **kwargs):
#     if created:
#         # Order yangi yaratildi
#         title = "Yangi order yaratildi"
#         body = f"Sizning orderingiz qabul qilindi: {instance.total} sum"
#     elif instance.status == "success":
#         title = "Order muvaffaqiyatli to‘landi"
#         body = f"Sizning orderingiz: {instance.total} sum to‘landi"
#     else:
#         return  # boshqa statuslar uchun push yubormaymiz
#
#     # User active device tokenlari
#     tokens = instance.user.fcmdevice_set.filter(is_active=True).values_list("token", flat=True)
#     for token in tokens:
#         Notifications.send_notification(token, title, body)
