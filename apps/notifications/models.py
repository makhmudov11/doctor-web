from django.db import models

from apps.users.models import CustomUser
from apps.utils.base_models import CreateUpdateBaseModel
class FcmDeviceChoice(models.TextChoices):
    IOS = 'ios', 'IOS'
    ANDROID = 'android', 'ANDROID'

class FCMDevice(CreateUpdateBaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, related_name='devices', null=True)
    token = models.CharField(max_length=100, unique=True, db_index=True)
    device_type = models.CharField(max_length=50, default='', choices=FcmDeviceChoice.choices, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} ----> {self.token}"


class Notification(CreateUpdateBaseModel):
    device = models.ForeignKey(FCMDevice, related_name='notifications',
                               on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, default='')
    message = models.TextField(default='', blank=True)
    data = models.JSONField(default=dict, blank=True)