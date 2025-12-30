from background_task import background
from django.utils import timezone

from apps.profile.models import Story


@background(schedule=60)
def update_status_for_expired_stories():
    expired_stories = Story.objects.filter(expires_at__lt=timezone.now(), status=False)

    for story in expired_stories:
        story.status = True
        story.save()