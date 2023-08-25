"""
This module defines custom permission classes for user with
Django REST framework.
"""

from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission to allow only the author to update the blog.
    """

    message = 'You must be the author to update the blog!'

    def has_object_permission(self, request, view, obj):
        my_safe_method = ['GET', 'PUT']
        if request.method in my_safe_method:
            return True
        return obj.author == request.user

