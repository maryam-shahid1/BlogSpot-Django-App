"""
URL patterns for student authentication and profile management.
"""

from django.urls import path

from comments.api.views import (CommentDetailAPIView, CommentListAPIView,
                                CreateCommentAPIView, UpdateCommentAPIView)

urlpatterns = [
    path('', CommentListAPIView.as_view(), name='comment_list'),
    path('<pk>/', CommentDetailAPIView.as_view(), name='comment_detail'),
    path('create/',
         CreateCommentAPIView.as_view(), name='create_comment'),
    path('update/<pk>/', UpdateCommentAPIView.as_view(), name='update'),
]

