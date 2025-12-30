from django.urls import path

from apps.profile.views.follows import (UserFollowListAPIView, UserUnfollowUserAPIView,
                                        UserFollowCreateAPIView, UserFollowerListAPIView)
from apps.profile.views.profiles import UserProfileRetrieveAPIView
from apps.profile.views.stories import UserStoryCreateAPIView, UserActiveStoryListAPIView, StoryMarkViewedAPIView, \
    UserStoryDeleteAPIView, UserStoryViewedAllListAPIView

app_name = 'profile'

urlpatterns = [
    path('detail/me/', UserProfileRetrieveAPIView.as_view(), name='profile-detail'),
    path('follow/<int:profile_public_id>/', UserFollowCreateAPIView.as_view(),
         name='patient-follow-user'),
    path('unfollow/<int:profile_public_id>/', UserUnfollowUserAPIView.as_view(),
         name='user-unfollow-user'),
    path('follow/list/', UserFollowListAPIView.as_view(), name='profile-follow-list'),
    path('followers/list/', UserFollowerListAPIView.as_view(), name='profile-followers-list'),
    path('story/create/', UserStoryCreateAPIView.as_view(), name='user-story-create'),
    path('active/story/', UserActiveStoryListAPIView.as_view(),
         name='doctor-active-story-list'),
    path('story/viewed/<int:story_id>/', StoryMarkViewedAPIView.as_view(), name='story-viewed'),
    path('story/delete/<int:story_id>/', UserStoryDeleteAPIView.as_view(), name='story-delete'),
    path('story/viewed/<int:story_id>/all/', UserStoryViewedAllListAPIView.as_view(), name='story-viewed-all'), # tekshirilmagan



    # path('list/', UserProfileListAPIView.as_view(), name='profile-list'),
    # path('story/list/', UserStoryListAPIView.as_view(), name='story_list'),
]
