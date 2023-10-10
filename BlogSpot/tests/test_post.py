"""
Module: users.api.tests.test_views
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


def get_organisation():
    org = Organisation.objects.create(
        id="1", org_name="Arbisoft2", website="https://www.arbisoft.com/"
    )
    return org


def get_user():
    org = get_organisation()
    author = User.objects.create_user(
        id="1",
        username="123",
        email="123@123.com",
        organisation=org,
        first_name="maryam",
        last_name="shahid",
    )
    author.set_password("12345678")
    author.save()
    return author


def get_image():
    image_content = b"Mock image content"
    image = SimpleUploadedFile("test_image.jpg", image_content)
    return image


def get_post():
    post = Post.objects.create(
        id="1",
        title="Post Title",
        author_id=1,
        organisation_id=1,
        content="Content",
        category="Technology",
        status="Approved",
        image=get_image(),
    )
    return post


class PostDetailAPIViewTest(TestCase):
    """
    Test class for user login functionality.
    """

    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.author = get_user()
        self.post = get_post()
        self.url = f"/api/posts/{self.post.id}/"

    def test_retrieve_post_with_valid_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["title"], "Post Title")

    def test_retrieve_post_with_invalid_id(self):
        id = 3
        response = self.client.get(f"/api/posts/{id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostCreateAPIViewTest(TestCase):
    """
    Test class for user login functionality.
    """

    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.author = get_user()
        self.post = get_post()
        self.url = "/api/posts/"

    def get_jwt_token(self):
        """
        Helper function to get JWT token.
        """
        refresh = RefreshToken.for_user(self.author)
        print(refresh.access_token)
        return str(refresh.access_token)

    def test_create_post_with_valid_data(self):
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        image_content = b"Mock image content"
        image = SimpleUploadedFile("test_image.jpg", image_content)

        org = Organisation.objects.create(
            id="2", org_name="Arbisoft2", website="https://www.arbisoft.com/"
        )

        author = User.objects.create_user(
            id="2",
            username="maryam",
            email="maryam@123.com",
            organisation=org,
            first_name="maryam",
            last_name="shahid",
        )
        author.set_password("12345678")
        author.save()

        data = {
            "title": "New post",
            "author": 2,  # Use the author's ID
            "organisation": 2,  # Use the organisation's ID
            "content": "Content",
            "category": "Technology",
            "status": "Draft",
            image: image,
        }

        response = self.client.post(self.url, data, format="multipart")
        print("RESPONSE: ", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["title"], "New post")

    def test_create_post_with_invalid_data(self):
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        image_content = b"Mock image content"
        image = SimpleUploadedFile("test_image.jpg", image_content)

        org = Organisation.objects.create(
            id="2", org_name="Arbisoft2", website="https://www.arbisoft.com/"
        )

        author = User.objects.create_user(
            id="2",
            username="maryam",
            email="maryam@123.com",
            organisation=org,
            first_name="maryam",
            last_name="shahid",
        )
        author.set_password("12345678")
        author.save()

        data = {
            "title": "",
            "author": 2,  # Use the author's ID
            "organisation": 2,  # Use the organisation's ID
            "content": "Content",
            "category": "Technology",
            "status": "Draft",
            image: image,
        }

        response = self.client.post(self.url, data, format="multipart")
        print("RESPONSE: ", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn(response.data["title"], "New post")


class PostUpdateAPIViewTest(TestCase):
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.author = get_user()
        self.post = get_post()
        self.url = f"/api/posts/{self.post.id}/"

    def get_jwt_token(self):
        """
        Helper function to get JWT token.
        """
        refresh = RefreshToken.for_user(self.author)
        print(refresh.access_token)
        return str(refresh.access_token)

    def test_update_post_with_token(self):
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"title": "Updated Title"}
        response = self.client.patch(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["title"], "Updated Title")

    def test_update_post_without_token(self):
        token = ""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"title": "Updated Title"}
        response = self.client.patch(
            f"/api/posts/{self.post.id}/", data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostDeleteAPIViewTest(TestCase):
    def setUp(self):
        """
        Set up test data and client.
        """
        self.client = APIClient()
        self.post = get_post()
        self.author = get_user()
        self.url = f"/api/posts/{self.post.id}/soft_delete/"

    def get_jwt_token(self):
        """
        Helper function to get JWT token.
        """
        refresh = RefreshToken.for_user(self.author)
        return str(refresh.access_token)

    def test_delete_post_with_token(self):
        token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.put(self.url, {"is_deleted": True}, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["detail"], "Soft-deleted successfully.")

    def test_delete_post_without_token(self):
        token = ""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.put(
            self.url,
            {"is_deleted": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
