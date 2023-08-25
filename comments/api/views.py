from django.db.models import Q
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from comments.api.permissions import IsUserOrReadOnly
from comments.api.serializers import (CommentSerializer,
                                      CreateCommentSerializer,
                                      UpdateCommentSerializer,
                                      CommentDetailSerializer)
from comments.models import Comment


class CommentListAPIView(ListAPIView):
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
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content']
    permission_classes = [IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query)
            ).distinct()
        return queryset_list


class CommentDetailAPIView(RetrieveAPIView):
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
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAdminUser]


class CreateCommentAPIView(CreateAPIView):
    """
    Create a comment.

    # Example Request:
    POST /api/comments/create/

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
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateCommentAPIView(RetrieveUpdateAPIView):
    """
    Update a comment.

    ### Example Request:
        PUT /api/comments/1/update/

    ### Example Response:
        {
            "response_code": 200,
            "data": {
                "content": "nice blog!!",
                "date": "2023-08-23T09:18:24.681870Z"
            }
        }
    """
    queryset = Comment.objects.all()
    serializer_class = UpdateCommentSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()

