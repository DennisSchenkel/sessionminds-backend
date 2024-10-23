from django.contrib.auth.models import User
from .models import Vote
from tools.models import Tool
from topics.models import Topic
from rest_framework import status
from rest_framework.test import APITestCase


class VotesTest1ListView(APITestCase):
    """
    Test to get all votes, create a vote,
    and create a vote when user is unauthenticated

    Args:
        APITestCase: Inherits from APITestCase class.
        """
    def setUp(self):
        # Define user data
        self.user_data = {
            "email": "voteuser@example.com",
            "password": "VoteUser1234!!"
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
            short_description="Short description",
            full_description="Full description",
            instructions="Instructions",
            user=self.user,
            topic=self.topic
        )
        # Login user
        login_url = "/login/"
        login_response = self.client.post(login_url, {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }, format="json")
        self.access_token = login_response.data.get("access")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )

    # Test to get all votes
    def test_1_get_all_votes(self):
        print("\nVotes Test 1: Get all votes")
        Vote.objects.create(user=self.user, tool=self.tool)
        self.client.credentials()
        response = self.client.get("/votes/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        print("Test passed \n")

    # Test to create a vote
    def test_2_create_vote_authenticated(self):
        print("\nVotes Test 2: Create a vote")
        response = self.client.post("/votes/", {
            "tool": self.tool.id
        }, format="json")
        count = Vote.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count, 1)
        print("Test passed \n")

    # Test to create a vote when user is unauthenticated
    def test_3_create_vote_unauthenticated(self):
        print("\nVotes Test 3: Create a vote unauthenticated")
        self.client.credentials()
        response = self.client.post("/votes/", {
            "tool": self.tool.id
        }, format="json")
        count = Vote.objects.count()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(count, 0)
        print("Test passed \n")


class VotesTest2DetailsView(APITestCase):
    """
    Test to retrieve a vote, delete a vote,
    and delete a vote when user is not the owner

    Args:
        APITestCase: Inherits from APITestCase class.
    """
    def setUp(self):
        # Define user data
        self.user_data = {
            "email": "votedetailuser@example.com",
            "password": "VoteDetail1234!!"
        }
        # Create user
        self.user = User.objects.create_user(
            username=self.user_data["email"],
            email=self.user_data["email"],
            password=self.user_data["password"]
        )
        # Create topic
        self.topic = Topic.objects.create(title="Detail Topic")
        # Create tool
        self.tool = Tool.objects.create(
            title="Detail Tool",
            short_description="Short description",
            full_description="Full description",
            instructions="Instructions",
            user=self.user,
            topic=self.topic
        )
        # Create vote
        self.vote = Vote.objects.create(user=self.user, tool=self.tool)
        # Login user
        login_url = "/login/"
        login_response = self.client.post(login_url, {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }, format="json")
        self.access_token = login_response.data.get("access")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )

    # Test to retrieve a vote
    def test_4_retrieve_vote(self):
        print("\nVotes Test 4: Retrieve a vote")
        response = self.client.get(f"/votes/{self.vote.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.vote.id)
        print("Test passed \n")

    # Test to delete a vote
    def test_5_delete_vote_owner(self):
        print("\nVotes Test 5: Delete a vote owner")
        response = self.client.delete(f"/votes/{self.vote.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("Test passed \n")

    # Test to delete a vote when user is not the owner
    def test_6_delete_vote_non_owner(self):
        print("\nVotes Test 6: Delete a vote non-owner")
        User.objects.create_user(
            username="voteuser2@example.com",
            email="voteuser2@example.com",
            password="VoteUser21234!!"
        )
        login_url = "/login/"
        login_response = self.client.post(login_url, {
            "email": "voteuser2@example.com",
            "password": "VoteUser21234!!"
        }, format="json")
        access_token2 = login_response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token2}")
        response = self.client.delete(f"/votes/{self.vote.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("Test passed \n")


class VotesTest3VotesByTool(APITestCase):
    """
    Test to get votes by tool

    Args:
        APITestCase: Inherits from APITestCase class.
    """
    def setUp(self):
        # Define user data
        self.user_data = {
            "email": "votedetailuser@example.com",
            "password": "VoteDetail1234!!"
        }
        # Create user
        self.user = User.objects.create_user(
            username=self.user_data["email"],
            email=self.user_data["email"],
            password=self.user_data["password"]
        )
        # Create topic
        self.topic = Topic.objects.create(title="Votes Topic")
        # Create tool
        self.tool = Tool.objects.create(
            title="Tool Votes",
            short_description="Short description",
            full_description="Full description",
            instructions="Instructions",
            user=self.user,
            topic=self.topic
        )
        # Create vote
        self.vote = Vote.objects.create(user=self.user, tool=self.tool)

    # Test to get votes by tool
    def test_7_get_votes_by_tool(self):
        print("\nVotes Test 8: Get votes by tool")
        response = self.client.get(
            f"/votes/tool/{self.tool.id}/", format="json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if user has voted
        self.assertFalse(response.data["user_has_voted"])
        self.assertIsNone(response.data["vote_id"])
        print("Test passed \n")

    # Test to get votes by tool with 50 votes
#    def test_8_get_votes_by_tool_with_50_votes(self):
#        print("\nVotes Test 8: Get votes by tool with 50 votes")
        # Create 500 votes with different users
#        for i in range(500):
#            user = User.objects.create_user(
#                username=f"user{i}@example.com",
#                email=f"user{i}@example.com",
#                password="TestUser1234!!"
#            )
#            Vote.objects.create(user=user, tool=self.tool)
#        response = self.client.get(
#            f"/votes/tool/{self.tool.id}/", format="json"
#            )
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        # Check if user has voted
#        self.assertFalse(response.data["user_has_voted"])
#        self.assertIsNone(response.data["vote_id"])
#        print("Test passed \n")
