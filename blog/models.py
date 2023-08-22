"""
This module contains post and comment models.
"""

from django.db import models
from django.utils import timezone

from user.models import Organisation, User


class Post(models.Model):
    PostStatusChoices = [
        ('Draft', 'Draft'),
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    CategoryChoices = [
        ('Technology', 'Technology'),
        ('Lifestyle', 'Lifestyle'),
        ('Food', 'Food'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(
        max_length=100,
        choices=PostStatusChoices,
        default='Draft')
    published_date = models.DateTimeField(default=timezone.now())
    slug = models.SlugField(unique=True)
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices,
        default='')
    is_public = models.BooleanField(default=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

