from django.contrib.auth.models import User
from .models import Tool
from categories.models import Category
from rest_framework import status
from rest_framework.test import APITestCase


class ToolsListViewTest(APITestCase):

    def setUp(self):
        User.objects.create_user(username="TestUser", password="1234Test")
        print("User created")
        Category.objects.create(title="Test Category")
        print("Category created")

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

    # Test to create a tool without being logged in
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


class ToolsDetailViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="TestUser",
            password="1234Test"
            )
        print("User created")
        self.category = Category.objects.create(title="Test Category")
        print("Category created")
        self.tool = Tool.objects.create(
            title="Test Tool",
            short_description="This is a old test tool",
            full_description="This is a old test tool",
            instructions="This is a old test tool",
            slug="test-tool",
            user=self.user
        )

    # Test to get a single tool by slug
    def test_get_single_tool(self):
        response = self.client.get(f"/tools/tool/{self.tool.slug}/")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("User can see a single tool")

    # Test to update a tool
    def test_update_tool(self):
        self.client.login(username="TestUser", password="1234Test")

        response = self.client.put(f"/tools/tool/{self.tool.slug}/", {
            "title": "Test Tool",
            "short_description": "This is a new test tool",
            "full_description": "This is a new test tool",
            "instructions": "This is a new test tool",
            "categories": [self.category.id]
        }, format='json')

        self.tool.refresh_from_db()

        print(response.data)
        self.assertEqual(
            self.tool.short_description,
            "This is a new test tool"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("User can update a tool")

    # Test to delete a tool
    def test_delete_tool(self):
        self.client.login(username="TestUser", password="1234Test")
        response = self.client.delete(f"/tools/tool/{self.tool.slug}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("User can delete a tool")

    # Test to update a tool without being owner
    def test_update_tool_not_owner(self):
        User.objects.create_user(username="TestUser2", password="1234Test")
        self.client.login(username="TestUser2", password="1234Test")
        response = self.client.put(f"/tools/tool/{self.tool.slug}/", {
            "title": "Test Tool",
            "short_description": "This is a new test tool",
            "full_description": "This is a new test tool",
            "instructions": "This is a new test tool",
            "categories": [self.category.id]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("User is not the owner and cannot update a tool")

    # Test to delete a tool without being owner
    def test_delete_tool_not_owner(self):
        User.objects.create_user(username="TestUser2", password="1234Test")
        self.client.login(username="TestUser2", password="1234Test")
        response = self.client.delete(f"/tools/tool/{self.tool.slug}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("User is not the owner and cannot delete a tool")
