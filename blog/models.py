"""
This module contains post and comment models.
"""

from django.db import models
from django.db.models import Model

from user.models import Organisation, User, TimeStampedModel

from blog.choices import PostStatusChoices, CategoryChoices


class Post(TimeStampedModel, Model):
    created_on = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(
        max_length=100,
        choices=PostStatusChoices.choices,
        default=PostStatusChoices.DRAFT,
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        default=CategoryChoices.TECHNOLOGY,
    )
    is_public = models.BooleanField(default=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
