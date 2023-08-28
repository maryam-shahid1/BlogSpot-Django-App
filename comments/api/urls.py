"""
URL patterns for student authentication and profile management.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from comments.api.views import CommentViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    *router.urls,
    path('comments/create/', CommentViewSet.as_view({'post': 'create'}), name='comment-create'),
    ]
