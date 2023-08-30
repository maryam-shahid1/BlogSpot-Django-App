"""
This module defines custom permission classes for user with
Django REST framework.
"""

from rest_framework.permissions import BasePermission


class IsUserOrReadOnly(BasePermission):
    message = 'You must be the author to update the profile!'

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj == request.user
