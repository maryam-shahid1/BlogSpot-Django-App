"""
This module registers custom user model.
"""

from django.contrib import admin

from .models import User

admin.site.register(User)