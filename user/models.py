"""
This module contains custom user and organisation's models.
"""

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email value must be set!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", 'Admin')
        extra_fields.setdefault("request_status", 'Accepted')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        organisation = extra_fields.get("organisation")

        user = self.create_user(email, password, **extra_fields)

        if organisation:
            user.organisation = organisation
            user.save(using=self._db)

        return user


class Organisation(models.Model):
    org_name = models.CharField(max_length=100)
    website = models.URLField(max_length=200, blank=True, null=True)


class User(AbstractBaseUser, PermissionsMixin):

    UserRoleChoices = [
        ('Admin', 'Admin'),
        ('Author', 'Author'),
    ]

    RequestStatusChoices = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(default=timezone.now())
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )
    request_status = models.CharField(
        max_length=100,
        choices=RequestStatusChoices
    )
    role = models.CharField(
        max_length=100,
        choices=UserRoleChoices,
        default='Author'
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
