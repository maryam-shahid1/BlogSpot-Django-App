"""
URL patterns for user.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from user.api.views import (
    LogoutView, UserLoginAPIView, 
    UserUpdateStatus, UserViewSet,
    )

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    *router.urls,
    path('user/login/', UserLoginAPIView.as_view(), name='login'),
    path('user/logout/', LogoutView.as_view(), name='logout'),
    path('user/<int:pk>/change-status/', UserUpdateStatus.as_view(), name='update_status'),
]

