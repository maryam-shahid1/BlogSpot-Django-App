"""
URL patterns for blog posts.
"""

from django.urls import path

from blog.api.views import (PendingPostDetailAPIView, PendingPostListAPIView,
                            PostCreateAPIView, PostDeleteAPIView,
                            PostDetailAPIView, PostDraftDetailAPIView,
                            DraftListAPIView, PostListAPIView,
                            PostUpdateAPIView)
from blog.views import blog

urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<slug>/update/', PostUpdateAPIView.as_view(), name='update'),
    path('<slug>/delete/', PostDeleteAPIView.as_view(), name='delete'),
    path('pending-posts/', PendingPostListAPIView.as_view(), name='pending'),
    path('pending-posts/<slug>/',
         PendingPostDetailAPIView.as_view(), name='pending_detail'),
    path('drafts/', DraftListAPIView.as_view(), name='draft_list'),
    path('drafts/<slug>/', PostDraftDetailAPIView.as_view(), name='draft'),
]

