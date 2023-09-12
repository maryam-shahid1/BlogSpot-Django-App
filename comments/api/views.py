from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from comments.api.serializers import (CommentSerializer,
                                      CreateCommentSerializer,
                                      CommentUpdateSerializer,
                                      CommentDetailSerializer)
from comments.api.permissions import IsUserOrReadOnly
from comments.models import Comment

from blog.api.pagination import PostPageNumberPagination


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    pagination_class = PostPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name', 'post__id']

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializer
        elif self.action == 'retrieve':
            return CommentDetailSerializer
        elif self.action == 'partial_update':
            return CommentUpdateSerializer
        elif self.action == 'update':
            return CommentUpdateSerializer
        return CreateCommentSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'retrieve':
            return [IsAdminUser()]
        elif self.action == 'destroy':
            return [IsUserOrReadOnly(), IsAdminUser()]
        elif self.action in ['update', 'partial_update']:
            return [IsUserOrReadOnly()]
        return super().get_permissions()

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

