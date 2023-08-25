from rest_framework.serializers import ModelSerializer, SerializerMethodField

from comments.models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user']


class CommentDetailSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user', 'content', 'date']


class CreateCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'content', 'date']


class UpdateCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'date']

