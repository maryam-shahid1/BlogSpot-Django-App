from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from comments.api.permissions import IsUserOrReadOnly
from comments.api.serializers import (CommentSerializer,
                                      CreateCommentSerializer,
                                      UpdateCommentSerializer,
                                      CommentDetailSerializer)
from comments.models import Comment


class CommentViewSet(ViewSet):
    
    def create(self, request):
        """
        Create a comment.

        # Example Request:
        POST /api/comment/create/

        # Example Response:
        {
            "response_code": 201,
            "data": {
                "post": 2,
                "content": "nice blog!",
                "date": "2023-08-23T09:18:24.681870Z"
            }
        }
        """
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    def list(self, request):
        """
        Fetch list of all comments.

        ### Example Request:
            GET /api/comments/
        
        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    "post": 2,
                    "user": 1,
                }
            }
        """
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Fetch details of a comment.

        ### Example Request:
            GET /api/comments/1/
        
        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    "post": 2,
                    "user": 1,
                    "content": "nice blog!",
                    "date": "2023-08-23T09:18:24.681870Z"
                }
            }
        """
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
        Update a comment.

        ### Example Request:
            PATCH /api/comments/22/

        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    "post": 5,
                    "user": 2,
                    "content": "nice",
                    "date": "2023-08-24T17:52:47.703441Z"
                }
            }
        """
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        self.check_object_permissions(request, comment)
        serializer = CommentDetailSerializer(
            comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

