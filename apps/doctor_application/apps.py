from django.apps import AppConfig


class DoctorApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.doctor_application'

    def ready(self):
        from . import signals