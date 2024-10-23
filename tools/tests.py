from django.contrib.auth.models import User
from .models import Tool
from topics.models import Topic
from rest_framework import status
from rest_framework.test import APITestCase


class ToolsTest1ListView(APITestCase):

    def setUp(self):
        # Define user data
        self.user_data = {
            "email": "testuser@example.com",
            "password": "TestUser1234!!"
        }

        # Create user
        self.user = User.objects.create_user(
            username=self.user_data["email"],
            email=self.user_data["email"],
            password=self.user_data["password"]
        )

        # Create topic
        self.topic = Topic.objects.create(title="Test Topic")

        # Login user
        login_url = "/login/"
        login_response = self.client.post(login_url, {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.access_token = login_response.data.get("access")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )

    # Test to get all tools
    def test_1_get_all_tools(self):
        print("\nTools Test 1: Get all tools")
        Tool.objects.create(
            title="Test Tool",
            short_description="This is a test tool",
            full_description="This is a test tool",
            instructions="This is a test tool",
            user=self.user,
            topic=self.topic
        )
        response = self.client.get("/tools/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test passed \n")

    # Test to create a tool
    def test_2_create_tool(self):
        print("\nTools Test 2: Create a tool")
        response = self.client.post("/tools/", {
            "title": "Test Tool",
            "short_description": "This is a test tool",
            "full_description": "This is a test tool",
            "instructions": "This is a test tool",
            "topic_id": self.topic.id
            }, format="json")
        count = Tool.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count, 1)
        print("Test passed \n")

    # Test to create a tool without being logged in
    def test_3_create_tool_not_logged_in(self):
        print("\nTools Test 3: Create a tool without being logged in")
        self.client.credentials()
        response = self.client.post("/tools/", {
            "title": "Test Tool",
            "short_description": "This is a test tool",
            "full_description": "This is a test tool",
            "instructions": "This is a test tool",
            "topic_id": self.topic.id
            }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("Test passed \n")


class ToolsTests2DetailView(APITestCase):
    def setUp(self):
        # Define user data
        self.user_data = {
            "email": "testuser@example.com",
            "password": "TestUser1234!!"
        }

        # Create user
        self.user = User.objects.create_user(
            username=self.user_data["email"],
            email=self.user_data["email"],
            password=self.user_data["password"]
        )

        # Create topic
        self.topic = Topic.objects.create(title="Test Topic")

        # Create tool
        self.tool = Tool.objects.create(
            title="Test Tool",
            short_description="This is a old test tool",
            full_description="This is a old test tool",
            instructions="This is a old test tool",
            slug="test-tool",
            user=self.user,
            topic=self.topic
        )

        # Login user
        login_url = "/login/"
        login_response = self.client.post(login_url, {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.access_token = login_response.data.get("access")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )

    # Test to get a single tool by slug
    def test_4_get_single_tool_by_slug(self):
        print("\nTools Test 4: Get a single tool by slug")
        response = self.client.get(
            f"/tools/tool/{self.tool.slug}/", format="json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test passed \n")

    # Test to get a single tool by id
    def test_5_get_single_tool_by_id(self):
        print("\nTools Test 5: Get a single tool by id")
        response = self.client.get(f"/tools/{self.tool.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test passed \n")

    # Test to update existing tool
    def test_6_update_tool(self):
        print("\nTools Test 6: Update a tool")
        response = self.client.put(f"/tools/{self.tool.id}/", {
            "title": "Test Tool",
            "short_description": "This is a new test tool",
            "full_description": "This is a new test tool",
            "instructions": "This is a new test tool",
            "topic_id": self.topic.id
        }, format="json")
        self.tool.refresh_from_db()
        self.assertEqual(
            self.tool.short_description,
            "This is a new test tool"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test passed \n")

    # Test to delete tool as owner
    def test_7_delete_tool(self):
        print("\nTools Test 7: Delete a tool")
        response = self.client.delete(f"/tools/{self.tool.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("Test passed \n")

    # Test to update tool without being owner
    def test_8_update_tool_not_owner(self):
        print("\nTools Test 8: Update a tool without being owner")
        user2 = User.objects.create_user(
            username="testuser2@example.com",
            email="testuser2@example.com",
            password="TestUser1234!!"
        )
        login_url = "/login/"
        login_response = self.client.post(login_url, {
            "email": user2.email,
            "password": "TestUser1234!!"
        }, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token2 = login_response.data.get("access")
        self.assertIsNotNone(access_token2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token2}")

        response = self.client.put(f"/tools/tool/{self.tool.slug}/", {
            "title": "Test Tool",
            "short_description": "This is a new test tool",
            "full_description": "This is a new test tool",
            "instructions": "This is a new test tool",
            "topic_id": self.topic.id
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("Test passed \n")

    # Test to delete tool without being owner
    def test_9_delete_tool_not_owner(self):
        print("\nTools Test 9: Delete a tool without being owner")
        user2 = User.objects.create_user(
            username="testuser2@example.com",
            email="testuser2@example.com",
            password="TestUser1234!!"
        )
        login_url = "/login/"
        login_response = self.client.post(login_url, {
            "email": user2.email,
            "password": "TestUser1234!!"
        }, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token2 = login_response.data.get("access")
        self.assertIsNotNone(access_token2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token2}")

        response = self.client.delete(
            f"/tools/tool/{self.tool.slug}/", format="json"
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("Test passed \n")
