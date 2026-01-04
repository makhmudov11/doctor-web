from django.urls import path

from apps.video.views import VideoCreateAPIView, VideoDestroyAPIView, ReelsCreateAPIView, VideoReactionAPIView, \
    VideoCommentCreateAPIView, VideoCommentListAPIView, DeleteVideoReelsCommentDestroyAPIView, \
    VideoReelsCommentReplyAPIView, VideoReelsCommentReplyListAPIView, CommentReactionAPIView, VideoAllListAPIView, \
    UserVideoListAPIView, ReelsAllListAPIView, UserReelsListAPIView, VideoReelsAddViewAPIView

app_name = 'content'

urlpatterns = [
    path('video/create/', VideoCreateAPIView.as_view(), name='video-create'),
    path('video-reels/delete/<int:video_id>/', VideoDestroyAPIView.as_view(), name='video-reels-delete'),
    path('reels/create/', ReelsCreateAPIView.as_view(), name='reels-create'),
    path('create/video-reels/reaction/<int:video_id>/', VideoReactionAPIView.as_view(),
         name='video-reaction'),
    path('video-reels/create/comment/<int:video_id>/', VideoCommentCreateAPIView.as_view(),
         name='video-comment-create'),
    path('video-reels/comment/list/<int:video_id>/', VideoCommentListAPIView.as_view(), name='video-comment-list'),
    path('video-reels/delete/comment/<int:comment_id>/', DeleteVideoReelsCommentDestroyAPIView.as_view(),
         name='delete-comment'),
    path('video-reels/comment/reply/create/<int:comment_id>/', VideoReelsCommentReplyAPIView.as_view(),
         name='comment-reply'),
    path('video-reels/comment/reply/list/<int:comment_id>/', VideoReelsCommentReplyListAPIView.as_view(),
         name='reply-comment-list'),
    path(
        'video-reels/comment/<int:comment_id>/reaction/', CommentReactionAPIView.as_view(), name='comment-reaction'),
    path('video/all/list/', VideoAllListAPIView.as_view(), name='all-video'),
    path('video/user/list/', UserVideoListAPIView.as_view(), name='user-video-all'),
    path('reels/all/list/', ReelsAllListAPIView.as_view(), name='all-reels'),
    path('reels/user/list/', UserReelsListAPIView.as_view(), name='user-reels-all'),
    path('video-reels/viewed/<int:content_id>/', VideoReelsAddViewAPIView.as_view(), name='video-reels-viewed'),
]
