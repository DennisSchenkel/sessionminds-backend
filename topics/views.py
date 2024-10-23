from django.db.models import Count
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from sessionminds.pagination import CustomPageNumberPagination
from .serializers import TopicSerializer
from tools.serializers import ToolSerializer
from .models import Topic
from tools.models import Tool
from rest_framework.permissions import AllowAny
from rest_framework import permissions


# Get all categories
class TopicsList(APIView):
    """
    A view for retrieving a list of categories.

    Inherits from APIView class.

    Methods:
        get(request): Retrieves all categories and returns serialized data.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Retrieve all categories and return serialized data.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The serialized category data.
        """
        ordering = request.query_params.get("ordering", "top")

        if ordering == "top":
            topics = Topic.objects.annotate(
                tool_count=Count("tools")
                ).order_by("-tool_count")
        else:
            topics = Topic.objects.all().order_by("title")

        paginator = CustomPageNumberPagination()
        paginated_topics = paginator.paginate_queryset(topics, request)

        serializer = TopicSerializer(paginated_topics, many=True)
        return paginator.get_paginated_response(serializer.data)


# Get single category by slug
class TopicDetailsBySlug(APIView):
    """
    A view to retrieve a specific category.

    This view allows to retrieve a category by its slug.

    Methods:
        get_object(slug):
            Check if category exists and return it or raise Http404.
        get(request, slug):
            Get category by slug and return it.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TopicSerializer

    # Check if category exists and return it or return 404
    # This method is only to validate the category exists
    def get_object(self, slug):
        """
        Check if category exists and return it or raise Http404.

        Args:
            slug (str): The slug of the category to retrieve

        Raises:
            Http404: If the category does not exist.

        Returns:
            Topic: The category object
        """
        try:
            topic = Topic.objects.get(slug=slug)
            self.check_object_permissions(self.request, topic)
            return topic
        except Topic.DoesNotExist:
            raise Http404

    # Get category by slug and return it
    # If category does exist, return it so it can be used
    def get(self, request, slug):
        """
        Retrieve a specific category.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The primary key of the category to retrieve.

        Returns:
            Response: The serialized category data.
        """
        topic = self.get_object(slug)
        serializer = TopicSerializer(
            topic, context={"request": request}
            )
        return Response(serializer.data)


# Get single category by id
class TopicDetailsById(APIView):
    """
    A view to retrieve a specific category.

    Args:
        APIView: The base APIView class.

    Raises:
        Http404: If the category does not exist.

    Returns:
        TopicDetailsById: The view to retrieve a specific category.
    """
    serializer_class = TopicSerializer

    # Check if category exists and return it or return 404
    def get_object(self, id):
        """
        Check if category exists and return it or raise Http404.

        Args:
            id (int): The primary key of the category to retrieve

        Raises:
            Http404: If the category does not exist.

        Returns:
            Topic: The category object
        """
        try:
            topic = Topic.objects.get(id=id).annotate(
                tool_count=Count("tools")
                )
            self.check_object_permissions(self.request, topic)
            return topic
        except Topic.DoesNotExist:
            raise Http404

    # Get category by id and return it
    def get(self, request, id):
        """
        Retrieve a specific category

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The primary key of the category to retrieve.

        Returns:
            Response: The serialized category data.
        """
        topic = self.get_object(id)
        serializer = TopicSerializer(
            topic, context={"request": request}
            )
        return Response(serializer.data)


# Get all tools by category slug
class ToolsOfTopicBySlug(APIView):
    """
    A view to retrieve a list of tools by category.

    Args:
        APIView: The base APIView class.

    Returns:
        ToolsOfTopicBySlug: The view to retrieve a list of tools by category.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ToolSerializer

    # Check if category exists and return it or return 404
    def get(self, request, slug):
        """
        Retrieve a list of tools by category

        Args:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the category to retrieve tools for.

        Returns:
            Response: The serialized tool data.
        """
        ordering = request.query_params.get("ordering", "latest")
        if ordering == "votes":
            tools = Tool.objects.filter(topic__slug=slug).annotate(
                vote_count=Count("votes")
                ).order_by("-vote_count")
        else:
            tools = Tool.objects.filter(topic__slug=slug).order_by("-created")

        paginator = CustomPageNumberPagination()
        paginated_tools = paginator.paginate_queryset(tools, request)

        serializer = ToolSerializer(
            paginated_tools, many=True, context={"request": request}
            )
        return paginator.get_paginated_response(serializer.data)
