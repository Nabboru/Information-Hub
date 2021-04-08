from django.urls import path
from .views import (PostCreateView, MyPostListView, PostDetailView, PostListView, PostUpdateView, PostDeleteView, AnnPostListView, AnnPostDetailView, CommentCreateView, LikeView, ReportView, CommentUpdateView, CommentDeleteView)
from .views import *

urlpatterns = [
    path('forum/', forum, name='forum'),
    path('forum-posts', PostListView.as_view(), name = 'forum-posts'),
    path('my-posts', MyPostListView.as_view(), name = 'my-posts'),
    path('create-post', PostCreateView.as_view(), name = 'create-post'),
    path('post/<int:pk>', PostDetailView.as_view(), name = 'post-details'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name = 'add-comment'),
    path('post/comment/<int:pk>/update/', CommentUpdateView.as_view(), name = 'edit-comment'),
    path('post/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name = 'delete-comment'),
    path('announcements', AnnPostListView.as_view(), name = 'announcements'),
    path('announcement/<int:pk>', AnnPostDetailView.as_view(), name = 'ann-post-details'),
    path('like/<int:pk>/', LikeView, name = 'like-post'),
    path('report/<int:pk>/', ReportView, name = 'report-post'),
]