"""
This module contains PostViewSet, DraftViewSet and PendingPostViewSet.
"""
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated)

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog.api.pagination import PostPageNumberPagination
from blog.api.permissions import IsAuthorOrReadOnly
from blog.api.serializers import (DraftListSerializer, DraftUpdateSerializer,
                                  PendingPostDetailSerializer,
                                  PostCreateSerializer, PostDetailSerializer,
                                  PostListSerializer, PostUpdateSerializer,
                                  PendingStatusUpdate)

from blog.models import Post
from comments.models import Comment
from comments.api.serializers import CreateCommentSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    """
    This viewset contains CRUD methods for blog posts.
    The method 'my_posts' is used to fetch all the posts made
    by the user.
    """
    pagination_class = PostPageNumberPagination
    queryset = Post.objects.filter(status='Approved')
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__first_name']
    
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'partial_update':
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        elif self.action == 'retrieve':
            return [AllowAny()]
        elif self.action == 'destroy':
            return [IsAuthorOrReadOnly(), IsAdminUser()]
        elif self.action == 'my_posts':
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'partial_update':
            return PostUpdateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return PostCreateSerializer

    def create(self, request):
        """
        Create a post.

        ### Example Request:
            POST /api/posts/create_post/

        ### Example Response:
        {
            "response_data": 201,
            data: {
                "title": "new blog",
                "content": "blogg",
                "category": "Technology",
                "status": "Pending"
            }
        }
        """
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            serializer.save(author=request.user,
                            organisation=request.user.organisation)
        return Response(serializer.data)

    def destroy(self, request):
        post = self.get_object()
        post.status = 'Deleted'
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def my_posts(self, request):
        queryset = Post.objects.filter(
            author=request.user,
            status__in=['Draft', 'Pending', 'Approved', 'Rejected']
        )
        page = self.paginate_queryset(queryset)
        # Serializing the paginated data
        if page is not None:
            serializer = PostDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)


class DraftViewSet(ModelViewSet):
    """
    This View Set contains CRUD methods for draft posts.
    """
    pagination_class = PostPageNumberPagination
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(
            status='Draft',
            author=user
        )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return DraftListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return DraftUpdateSerializer


class PendingPostViewSet(ModelViewSet):
    """
    This View Set contains CRUD methods for Pending posts,
    only visible to admin users.
    """
    pagination_class = PostPageNumberPagination
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__first_name']

    def get_queryset(self):
        organisation = self.request.user.organisation
        if self.request.user.is_staff:
            queryset = Post.objects.filter(
                organisation=organisation,
                status='Pending'
            )
            return queryset
        return Post.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'partial_update':
            return PendingPostDetailSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        # elif self.action == 'partial_update':
        #     return PendingPostDetailSerializer
        return PendingPostDetailSerializer
    
    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(
            post, data=request.data, partial=True)

        if serializer.is_valid():
            # Updating the status of the Post
            post.status = serializer.validated_data.get(
                'status', post.status)
            post.save()
            # Creating a new comment and associate it with the Post
            new_comment_data = serializer.validated_data.get('new_comment')
            if new_comment_data:
                Comment.objects.create(post=post, user=request.user, **new_comment_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

