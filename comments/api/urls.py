"""
URL patterns for student authentication and profile management.
"""

from django.urls import path

from comments.api.views import CommentViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    *router.urls,
    path('comment/create/', CommentViewSet.as_view({'post': 'create'}), name='comment-create'),
    ]
