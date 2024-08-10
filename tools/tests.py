from django.contrib.auth.models import User
from .models import Tool
from categories.models import Category
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APITestCase

class ToolsListViewTest(APITestCase):

    def setUp(self):
        User.objects.create_user(username="TestUser", password="1234Test")
        Category.objects.create(title="Test Category")
        print("User created")

    # Test to get all tools from the database and list them
    def test_get_all_tools(self):
        user = User.objects.get(username="TestUser")
        Tool.objects.create(
            title="Test Tool",
            short_description="This is a test tool",
            full_description="This is a test tool",
            instructions="This is a test tool",
            user=user
        )
        count = Tool.objects.count()
        response = self.client.get("/tools/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("User can see so many tools: " + str(count))
        print("User can see all tools")

    # Test to create a tool
    def test_create_tool(self):
        self.client.login(username="TestUser", password="1234Test")
        user = User.objects.get(username="TestUser")
        response = self.client.post("/tools/", {
            "title": "Test Tool",
            "short_description": "This is a test tool",
            "full_description": "This is a test tool",
            "instructions": "This is a test tool",
            "categories": [1],
            "user": user
            }
        )
        count = Tool.objects.count()
        print("Tools created by user: " + str(count))
        print(response.data)
        print("User can create a tool")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count, 1)

    def test_create_tool_not_logged_in(self):
        response = self.client.post("/tools/", {
            "title": "Test Tool",
            "short_description": "This is a test tool",
            "full_description": "This is a test tool",
            "instructions": "This is a test tool",
            "categories": [1],
            "user": 1
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("User is not logged in and cannot create a tool")