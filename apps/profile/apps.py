from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.profile'

    def ready(self):
        post_migrate.connect(self.run_task_after_migrate, sender=self)
        from . import signals

    def run_task_after_migrate(self, sender, **kwargs):
        from .tasks import update_status_for_expired_stories
        update_status_for_expired_stories(repeat=60)
