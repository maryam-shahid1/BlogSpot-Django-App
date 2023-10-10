"""
Description: This module contains test cases for the Users API app.
"""
from django.test import TestCase
from pytest import fixture
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from user.models import User, Organisation
from blog.models import Post
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


class UserRegisterPIViewTest(TestCase):
    """
    Test class for user login functionality.
    """

    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.url = "/api/users/"
        self.org = Organisation.objects.create(
            org_name="Arbisoft2", website="https://www.arbisoft.com/"
        )

    def test_create_valid_user(self):
        """
        Test user signup with valid credentials.
        """
        data = {
            "username": "123",
            "email": "123@123.com",
            "organisation": 1,
            "first_name": "maryam",
            "last_name": "shahid",
            "password": "testpassword",
        }

        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "123")

    def test_create_invalid_user(self):
        """
        Test user signup with invalid credentials.
        """
        data = {
            "username": "",
            "email": "123@123.com",
            "organisation": 1,
            "first_name": "maryam",
            "last_name": "shahid",
            "password": "testpassword",
        }

        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginAPIViewTest(TestCase):
    """
    Test class for user login functionality.
    """

    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.url = "/api/user/login/"
        self.org = Organisation.objects.create(
            org_name="Arbisoft2", website="https://www.arbisoft.com/"
        )

    def test_user(self):
        self.user = User.objects.create_user(
            username="123",
            email="123@123.com",
            organisation=self.org,
            first_name="maryam",
            last_name="shahid",
        )
        self.user.set_password("12345678")
        self.user.save()

    def test_user_login(self):
        """
        Test user login with valid credentials.
        """
        user = self.test_user()
        data = {"email": "123@123.com", "password": "12345678"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_login_with_incorrect_credentials(self):
        """
        Test user login with incorrect credentials.
        """
        data = {"email": "123@123.com", "password": "incorrectpassword"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)
