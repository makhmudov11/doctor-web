
# class Story(CreateUpdateBaseModel):
#     public_id = models.PositiveIntegerField(unique=True, db_index=True, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story')
#     role = models.CharField(
#         max_length=50,
#         choices=CustomUserRoleChoices.choices
#     )
#     content = models.FileField(upload_to='users/profile/story/', null=True)
#     content_type = models.CharField(max_length=100, null=True, choices=StoryChoices.choices)
#     view_count = models.PositiveIntegerField(default=0)
#     expires_at = models.DateTimeField(null=True, blank=True)
#     expired = models.BooleanField(default=False)  # for delete
#
#     def __str__(self):
#         return self.profile.full_name or ''
#
#     @property
#     def media_type(self):
#         if self.content:
#             ext = self.content.name.split('.')[-1].lower()
#             if ext in ['mp4', 'mov', 'avi']:
#                 return StoryChoices.VIDEO
#             elif ext in ['jpg', 'jpeg', 'png', 'gif']:
#                 return StoryChoices.IMAGE
#         return 'unknown'
#
#     def save(self, *args, **kwargs):
#         Story.objects.filter(
#             expires_at__lt=timezone.now(),
#             expired=False
#         ).update(expired=True)
#
#         if self.content:
#             ext = self.content.name.split('.')[-1].lower()
#             if ext in ['mp4', 'mov', 'avi']:
#                 self.content_type = StoryChoices.VIDEO
#             elif ext in ['jpg', 'jpeg', 'png', 'gif']:
#                 self.content_type = StoryChoices.IMAGE
#         if not self.expires_at:
#             self.expires_at = timezone.now() + timedelta(hours=24)
#         super().save(*args, **kwargs)
#
#     def is_expired(self):
#         return timezone.now() > self.expires_at
#
#     def mark_viewed(self, viewer_profile):
#         view, created = StoryView.objects.get_or_create(story=self, view_profile=viewer_profile)
#         if created:
#             self.view_count = StoryView.objects.filter(story=self).count()
#             self.save(update_fields=['view_count'])
#
#     class Meta:
#         db_table = 'story'
#         verbose_name = 'Story'
#         verbose_name_plural = 'Stories'
#         ordering = ['-created_at']
#
#
# class StoryView(CreateUpdateBaseModel):
#     story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_view')
#     view_profile = models.ForeignKey(BaseProfile, on_delete=models.CASCADE, related_name='viewed_stories')
#     viewed_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.view_profile.full_name} kordi {self.story.profile.full_name} ni storysini"
#
#     class Meta:
#         unique_together = ('story', 'view_profile')
#         ordering = ['-viewed_at']
#
#         db_table = 'story_view'
#         verbose_name = 'Story View'
#         verbose_name_plural = 'Story Viewers'
#
#
