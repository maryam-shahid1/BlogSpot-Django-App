from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from blog.api.permissions import IsAuthorOrReadOnly
from blog.api.serializers import (DraftListSerializer, DraftUpdateSerializer,
                                  PendingPostDetailSerializer,
                                  PendingPostListSerializer,
                                  PostCreateSerializer, PostDetailSerializer,
                                  PostListSerializer, PostUpdateSerializer)
from blog.models import Post


class PostViewSet(ViewSet):

    @action(detail=False, methods=['POST'])
    def create_post(self, request):
        """
        Create a post.

        ### Example Request:
            POST /api/blogs/posts/create_post/

        ### Example Response:
        {
            "response_data": 201,
            data: {
                "title": "new blog",
                "slug": "this-is-my-new",
                "content": "blogg",
                "category": "Technology",
                "status": "Pending"
            }
        }
        """
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user,
                        organisation=request.user.organisation)
        return Response(serializer.data)

    def list(self, request):
        """
        Fetch list of approved posts.

        ### Example Request:
            GET /api/blogs/posts/

        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    {
                        "id": 1,
                        "author": 2,
                        "organisation": 2,
                        "title": "My first blog 2"
                    },
                }
            }
        """
        queryset = Post.objects.filter(status='Approved')
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Fetch detail of a particular post.

        ### Example Request:
            GET /api/blogs/posts/5/

        ### Example Response:
        {
            "response_data": 200,
            data: {
                "id": 13,
                "title": "new blog",
                "slug": "this-is-my-new",
                "content": "blogg",
                "category": "Technology",
                "status": "Pending",
                "published_date": "2023-08-25T06:17:06.170561Z",
                "comments": [...]
            }
        }
        """
        queryset = Post.objects.filter(status='Approved')
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
        Update a post.

        ### Example Request:
            PATCH /api/blogs/posts/5/

        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "title": "patch",
                "content": "clean content",
            }
        }
        """
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serializer = PostUpdateSerializer(
            post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Delete a post.

        ### Example Request:
            DELETE /api/blogs/posts/7/

        ### Example Response:
        {
            "response_code": 204,
            "data": {}
        }
        """
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        if request.user == post.author or request.user.is_staff:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            "detail": "You do not have permission to delete this post."},
            status=status.HTTP_403_FORBIDDEN
        )


class DraftViewSet(ViewSet):

    def list(self, request):
        """
        Fetch list of user drafts.

        ### Example Request:
            GET /api/blogs/drafts/6

        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    "title": "maryam's blog",
                    "status": "Draft",
                }
            }

        """
        queryset = Post.objects.filter(status='Draft')
        serializer = DraftListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Fetch details of a draft.

        ### Example Request:
            GET /api/blogs/drafts/6/

        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "id": 14,
                "title": "maryam's blog",
                "slug": "maryam-blog",
                "content": "this is my first blog!!",
                "category": "Technology",
                "status": "Draft"
            }
        }
        """
        queryset = Post.objects.filter(status='Draft')
        draft = get_object_or_404(queryset, pk=pk)
        serializer = PostDetailSerializer(draft)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
        Update a draft.

        ### Example Request:
            PATCH /api/blogs/drafts/11/

        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    {
                        "title": "New Blog",
                        "content": "blog content is here",
                        "category": "Technology",
                        "status": "Draft"
                    }
                }
            }
        """
        draft = get_object_or_404(Post, pk=pk)
        serializer = DraftUpdateSerializer(
            draft, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PendingPostViewSet(ViewSet):

    def list(self, request):
        """
        Fetch list of all blogs pending for approval.

        ### Example Request:
            GET /api/blogs/pending-posts/

        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    "id": 9,
                    "author": 2,
                    "title": "pending",
                }
            }
        """
        queryset = Post.objects.filter(status='Pending')
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        ### Example Request:
           GET /api/blogs/pending-posts/8/

        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    "author": 2,
                    "category": "Technology",
                    "title": "pending",
                    "content": "oending posttttt",
                    "status": "Approved",
                    "comments": []  #Comments by admin in case of rejection
                }
            }
        """
        queryset = Post.objects.filter(status='Pending')
        pending = get_object_or_404(queryset, pk=pk)
        serializer = PostDetailSerializer(pending)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
        ### Example Request:
           PATCH /api/blogs/pending-posts/8/

        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    "author": 2,
                    "category": "Technology",
                    "title": "pending",
                    "content": "oending posttttt",
                    "status": "Approved",
                    "comments": []  #Comments by admin in case of rejection
                }
            }
        """
        pending_post = get_object_or_404(Post, pk=pk)
        serializer = PendingPostDetailSerializer(
            pending_post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

