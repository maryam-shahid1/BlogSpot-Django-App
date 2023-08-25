"""
This module defines serializers for the Blog and Comment models using Django
REST framework.
"""

from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField)

from blog.models import Post
from comments.api.serializers import CommentSerializer


class PostCreateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
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
            'organisation',
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
            'slug',
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
            'title',
            'status',
        ]


class DraftUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'content',
            'category',
            'status',
        ]

class PendingPostListSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'id',
            'slug',
            'author',
            'title',
        ]


class PendingPostDetailSerializer(ModelSerializer):
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'content',
            'status',
            'comments',
        ]

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        return CommentSerializer(comments, many=True).data

