from django.db.models import Q
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveDestroyAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from blog.api.permissions import IsAuthorOrReadOnly
from blog.api.serializers import (PendingPostDetailSerializer,
                                  PendingPostListSerializer,
                                  PostCreateUpdateSerializer,
                                  PostDetailSerializer, PostListSerializer,
                                  DraftListSerializer)
from blog.models import Post


class PostCreateAPIView(CreateAPIView):
    """
    Create a post.

    ### Example Request:
        POST /api/blogs/create/

    ### Example Response:
    {
        "response_data": 201,
        data: {
            "id": 13,
            "title": "new blog",
            "slug": "this-is-my-new",
            "content": "blogg",
            "category": "Technology",
            "status": "Pending",
        }
    }
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        organisation=self.request.user.organisation)


class PostListAPIView(ListAPIView):
    """
    Fetch list of approved posts.

    ### Example Request:
        GET /api/blogs/

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
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__first_name']
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.filter(status='Approved')
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__first_name__icontains=query)
            ).distinct()
        return queryset_list


class PostDetailAPIView(RetrieveAPIView):
    """
    Fetch detail of a particular post.

    ### Example Request:
        GET /api/blogs/this-is-my-new/

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
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        serializer.save()


class PostUpdateAPIView(RetrieveUpdateAPIView):
    """
    Update a post.

    ### Example Request:
        PUT /api/blogs/new-blog/update/

    ### Example Response:
    {
        "response_code": 200,
        "data": {
             "id": 9,
            "title": "NEW BLOGGY",
            "slug": "new-blog",
            "content": "this is my test blog which was updated...!!",
            "category": "Lifestyle",
            "status": "Approved"
        }
    }
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def perform_update(self, serializer):
        serializer.save(author=self.request.user,
                        organisation=self.request.user.organisation)


class PostDeleteAPIView(RetrieveDestroyAPIView):
    """
    Delete a post.

    ### Example Request:
        DELETE /api/blogs/new-blog/delete/

    ### Example Response:
    {
        "response_code": 204,
        "data": {}
    }
    """
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, IsAuthorOrReadOnly]
    lookup_field = 'slug'


class DraftListAPIView(ListAPIView):
    """
    Fetch list of user drafts.

    ### Example Request:
        GET /api/blogs/drafts/hira-blog

    ### Example Response:
        {
            "response_code": 200,
            "data": {
                "title": "hira's blog",
                "status": "Draft",
            }
        }

    """
    queryset = Post.objects.filter(status='Draft')
    serializer_class = DraftListSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class PostDraftDetailAPIView(RetrieveUpdateAPIView):
    """
    Fetch details of a draft.

    ### Example Request:
        PUT /api/blogs/drafts/maryam-blog/

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
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def perform_update(self, serializer):
        serializer.save(author=self.request.user,
                        organisation=self.request.user.organisation)


class PendingPostListAPIView(ListAPIView):
    """
    Fetch list of all blogs pending for approval.

    ### Example Request:
        GET /api/blogs/pending-posts/
    
    ### Example Response:
        {
            "response_code": 200,
            "data": {
                "id": 9,
                "slug": "my-post",
                "author": 2,
                "title": "pending",
            }
        }
    """
    serializer_class = PendingPostListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user_organisation = self.request.user.organisation
        queryset = Post.objects.filter(
            status='Pending', organisation=user_organisation)
        return queryset


class PendingPostDetailAPIView(RetrieveUpdateAPIView):
    """
    ### Example Request:
        PUT /api/blogs/pending-posts/pending/
    
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
    serializer_class = PendingPostDetailSerializer
    queryset = Post.objects.filter(status='Pending')
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        if 'new_comment' in serializer.validated_data:
            serializer.create(serializer.validated_data)
        else:
            serializer.save()

