"""
This module contains serializers for User CRUD and Login.
"""

from rest_framework.serializers import (ModelSerializer, EmailField,
                                        CharField, ValidationError)

from user.models import User


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email address')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'organisation',
            'username',
            'password',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_email(self, value):
        email = value
        user_queryset = User.objects.filter(email=email)
        if user_queryset.exists():
            raise ValidationError("This user has already been registered!")
        return value


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        username = data.get('username', None)
        password = data['password']
        if not username:
            raise ValidationError('Username Required.')
        user = User.objects.filter(username=username)
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('This username is not valid.')
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect credentials.')
        return data


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'request_status'
        ]


class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }


class UserStatusUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'organisation',
            'username',
            'role',
            'request_status',
        ]
        read_only_fields = [
            'first_name',
            'last_name',
            'email',
            'organisation',
            'username',
        ]
