"""
URL patterns for blog posts.
"""

from django.urls import path
from django.views.decorators.http import require_GET
from rest_framework.routers import DefaultRouter

from blog.api.views import DraftViewSet, PendingPostViewSet, PostViewSet
from blog.views import blog

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='posts')
router.register(r'drafts', DraftViewSet, basename='drafts')
router.register(r'pending-posts', PendingPostViewSet, basename='pending')

urlpatterns = router.urls

