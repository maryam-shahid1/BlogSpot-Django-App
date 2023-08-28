"""
This module defines serializers for the Blog and Comment models using Django
REST framework.
"""

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from blog.models import Post
from comments.api.serializers import CommentSerializer, CreateCommentSerializer


class PostCreateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'category',
            'status',
        ]


class PostUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
        ]


class PostListSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
        ]


class PostDetailSerializer(ModelSerializer):
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'author',
            'organisation',
            'title',
            'status',
            'content',
            'published_date',
            'comments'
        ]

    def get_comments(self, obj):
        """
        Retrieve comments related to the current Post instance.
        """
        comments = obj.comment_set.all()
        return CommentSerializer(comments, many=True).data


class DraftListSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
        ]


class DraftUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
            'status',
        ]


class PendingPostDetailSerializer(ModelSerializer):
    comments = SerializerMethodField()
    new_comment = CreateCommentSerializer(write_only=True)
    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'content',
            'status',
            'comments',
            'new_comment'
        ]
        read_only_fields = (
            'author',
            'category',
            'title',
            'content',
            'comments',
        )

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        return CommentSerializer(comments, many=True).data


class PendingStatusUpdate(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'status'
        ]
