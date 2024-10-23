from django.contrib.auth.models import User
from .models import Comment
from tools.models import Tool
from topics.models import Topic
from rest_framework import status
from rest_framework.test import APITestCase


class CommentsTest1ToolComments(APITestCase):

    def setUp(self):
        # Create a user with first and last name
        self.user_with_names = User.objects.create_user(
            username="user_with_names@example.com",
            email="user_with_names@example.com",
            password="UserWithNames123!!"
        )
        # Update the existing profile instead of creating a new one
        self.user_with_names.profile.first_name = "John"
        self.user_with_names.profile.last_name = "Doe"
        self.user_with_names.profile.save()

        # Create a user without first and/or last name
        self.user_without_names = User.objects.create_user(
            username="user_without_names@example.com",
            email="user_without_names@example.com",
            password="UserWithoutNames123!!"
        )
        # Update the existing profile to have empty first and last names
        self.user_without_names.profile.first_name = ""
        self.user_without_names.profile.last_name = ""
        self.user_without_names.profile.save()

        # Create a tool
        self.topic = Topic.objects.create(title="Test Topic")
        self.tool = Tool.objects.create(
            title="Test Tool",
            short_description="Short description",
            full_description="Full description",
            instructions="Instructions",
            user=self.user_with_names,
            topic=self.topic
        )

    def test_1_create_comment_with_names(self):
        print(
            "\nComments Test 1: Create a comment as user with names"
        )
        # Authenticate as user_with_names
        login_url = "/login/"
        login_response = self.client.post(
            login_url,
            {
                "email": "user_with_names@example.com",
                "password": "UserWithNames123!!"
            },
            format="json"
        )
        self.assertEqual(
            login_response.status_code, status.HTTP_200_OK
        )
        access_token = login_response.data.get("access")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        # Create a comment
        response = self.client.post(
            f"/comments/tool/{self.tool.id}/",
            {"text": "This is a valid comment."},
            format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(
            Comment.objects.get().text, "This is a valid comment."
        )
        print("Test passed \n")

    def test_2_create_comment_without_names(self):
        print(
            "\nComments Test 2: Create a comment as user without names"
        )
        # Authenticate as user_without_names
        login_url = "/login/"
        login_response = self.client.post(
            login_url,
            {
                "email": "user_without_names@example.com",
                "password": "UserWithoutNames123!!"
            },
            format="json"
        )
        self.assertEqual(
            login_response.status_code, status.HTTP_200_OK
        )
        access_token = login_response.data.get("access")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        # Attempt to create a comment
        response = self.client.post(
            f"/comments/tool/{self.tool.id}/",
            {"text": "This comment should fail."},
            format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(Comment.objects.count(), 0)
        print("Test passed \n")

    def test_3_create_comment_unauthenticated(self):
        print(
            "\nComments Test 3: Create a comment as unauthenticated user"
        )
        # Remove authentication
        self.client.credentials()

        # Attempt to create a comment
        response = self.client.post(
            f"/comments/tool/{self.tool.id}/",
            {"text": "This comment should not be created."},
            format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(Comment.objects.count(), 0)
        print("Test passed \n")

    def test_4_get_all_comments(self):
        print("\nComments Test 4: Get all comments for a tool")
        # Create multiple comments
        Comment.objects.create(
            tool=self.tool,
            user=self.user_with_names,
            text="First comment."
        )
        Comment.objects.create(
            tool=self.tool,
            user=self.user_with_names,
            text="Second comment."
        )
        response = self.client.get(
            f"/comments/tool/{self.tool.id}/",
            format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.data.get("results", [])), 2
        )
        self.assertEqual(
            response.data["results"][0]["text"], "Second comment."
            )
        self.assertEqual(
            response.data["results"][1]["text"], "First comment."
            )
        print("Test passed \n")


class CommentsTest2CommentDetails(APITestCase):

    def setUp(self):
        # Create a user with first and last name (owner)
        self.owner_user = User.objects.create_user(
            username="owner_user@example.com",
            email="owner_user@example.com",
            password="OwnerUser123!!"
        )
        # Update the existing profile
        self.owner_user.profile.first_name = "Alice"
        self.owner_user.profile.last_name = "Smith"
        self.owner_user.profile.save()

        # Create another user with first and last name
        self.other_user = User.objects.create_user(
            username="other_user@example.com",
            email="other_user@example.com",
            password="OtherUser123!!"
        )
        # Update the existing profile
        self.other_user.profile.first_name = "Bob"
        self.other_user.profile.last_name = "Johnson"
        self.other_user.profile.save()

        # Create a tool
        self.topic = Topic.objects.create(title="Detail Topic")
        self.tool = Tool.objects.create(
            title="Detail Tool",
            short_description="Short description",
            full_description="Full description",
            instructions="Instructions",
            user=self.owner_user,
            topic=self.topic
        )

        # Create a comment by owner_user
        self.comment = Comment.objects.create(
            tool=self.tool,
            user=self.owner_user,
            text="Owner's comment."
        )

    def test_5_retrieve_comment(self):
        print("\nComments Test 5: Retrieve a comment by ID")
        response = self.client.get(
            f"/comments/{self.comment.id}/",
            format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["id"], self.comment.id
        )
        self.assertEqual(
            response.data["text"], "Owner's comment."
        )
        print("Test passed \n")

    def test_6_delete_comment_owner(self):
        print(
            "\nComments Test 6: Delete a comment as the owner"
        )
        # Authenticate as owner_user
        login_url = "/login/"
        login_response = self.client.post(
            login_url,
            {
                "email": "owner_user@example.com",
                "password": "OwnerUser123!!"
            },
            format="json"
        )
        self.assertEqual(
            login_response.status_code, status.HTTP_200_OK
        )
        access_token = login_response.data.get("access")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        # Delete the comment
        response = self.client.delete(
            f"/comments/{self.comment.id}/",
            format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Comment.objects.count(), 0)
        print("Test passed \n")

    def test_7_delete_comment_non_owner(self):
        print(
            "\nComments Test 7: Delete a comment as a non-owner"
        )
        # Authenticate as other_user
        login_url = "/login/"
        login_response = self.client.post(
            login_url,
            {
                "email": "other_user@example.com",
                "password": "OtherUser123!!"
            },
            format="json"
        )
        self.assertEqual(
            login_response.status_code, status.HTTP_200_OK
        )
        access_token = login_response.data.get("access")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        # Attempt to delete the comment
        response = self.client.delete(
            f"/comments/{self.comment.id}/",
            format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(Comment.objects.count(), 1)
        print("Test passed \n")
