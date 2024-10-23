from django.contrib.auth.models import User
from .models import Topic
from tools.models import Tool
from rest_framework import status
from rest_framework.test import APITestCase


class TopicsTest1ListView(APITestCase):

    def setUp(self):
        # Create topics
        Topic.objects.create(title="Test Topic 1")
        Topic.objects.create(title="Test Topic 2")

    # Test to get all topics
    def test_1_get_all_topics(self):
        print("\nTopics Test 1: Get all topics")
        response = self.client.get("/topics/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        print("Test passed \n")


class TopicsTest2DetailsBySlug(APITestCase):

    def setUp(self):
        # Create a topic with a unique title and slug
        self.topic = Topic.objects.create(
            title="Unique Topic", slug="unique-topic"
            )

    # Test to get a topic by slug
    def test_2_get_topic_by_slug(self):
        print("\nTopics Test 2: Get topic by slug")
        response = self.client.get(
            f"/topics/{self.topic.slug}/", format="json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Unique Topic")
        print("Test passed \n")


class TopicsTest3ToolsOfTopicBySlugTest(APITestCase):

    def setUp(self):
        # Create a topic
        self.topic = Topic.objects.create(
            title="Tools Topic", slug="tools-topic"
            )
        # Create tools
        Tool.objects.create(
            title="Tool 1",
            short_description="Short desc 1",
            full_description="Full desc 1",
            instructions="Instructions 1",
            user=User.objects.create_user(
                username="user1", password="pass1234"
                ),
            topic=self.topic
        )
        Tool.objects.create(
            title="Tool 2",
            short_description="Short desc 2",
            full_description="Full desc 2",
            instructions="Instructions 2",
            user=User.objects.create_user(
                username="user2", password="pass1234"
                ),
            topic=self.topic
        )

    # Test to get all tools of a topic
    def test_3_get_tools_of_topic_by_slug(self):
        print("\nTopics Test 3: Get tools of topic by slug")
        response = self.client.get(
            f"/topics/list/{self.topic.slug}/", format="json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        print("Test passed \n")
