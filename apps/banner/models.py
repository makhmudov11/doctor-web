from django.db import models

from apps.utils.base_models import CreateUpdateBaseModel

class BannerChoices(models.TextChoices):
    ELON = 'elon', 'Elon'
    LINK = 'link', 'Link'

class Banner(CreateUpdateBaseModel):
    image = models.ImageField(upload_to='banner/', null=True)
    title = models.CharField(max_length=255, null=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True, default=None)
    _type = models.CharField(default=BannerChoices.ELON, choices=BannerChoices.choices, db_index=True)
    status = models.BooleanField(default=True, blank=True)

    class Meta:
        db_table = 'banner'
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pk} ----- {self.title or self.description} ----- {self._type}"