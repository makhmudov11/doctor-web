from django.db import models


from apps.utils.base_models import CreateUpdateBaseModel


class Service(CreateUpdateBaseModel):
    name = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(upload_to='services/', null=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ---- {self.description or self.image}"
