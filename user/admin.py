"""
This module registers custom user model.
"""

from django.contrib import admin

from user.models import Organisation, User

admin.site.register(User)
admin.site.register(Organisation)
