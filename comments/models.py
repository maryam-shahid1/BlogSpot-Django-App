from django.db import models

from blog.models import Post
from user.models import User, TimeStampedModel


class Comment(TimeStampedModel, models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

