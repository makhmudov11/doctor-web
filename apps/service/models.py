from django.db import models


from apps.utils.base_models import CreateUpdateBaseModel
from django.utils.translation import gettext_lazy as _

class Service(CreateUpdateBaseModel):
    name = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(upload_to='services/', null=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'services'
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ---- {self.description or self.image}"


class SocialNetwork(CreateUpdateBaseModel):
    title = models.CharField(max_length=255, null=True, verbose_name=_("Tarmoq nomi"))
    image = models.ImageField(null=True, blank=True, upload_to='social_network/', verbose_name=_("Rasm"))
    link = models.URLField(null=True, verbose_name=_("Tarmoq yo'li"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Tarmoq haqida"))
    status = models.BooleanField(default=True, verbose_name=_("Holati"))

    def __str__(self):
        return f"{self.title} --- {self.link}"

    class Meta:
        db_table = 'social_network'
        verbose_name = 'Social Network'
        ordering = ['-created_at']
