from django.db.models import Count
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from sessionminds.pagination import CustomPageNumberPagination
from .serializers import TopicSerializer, IconSerializer
from tools.serializers import ToolSerializer
from .models import Topic, Icon
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


class TopicDetailsById(APIView):
    serializer_class = TopicSerializer

    def get_object(self, id):
        try:
            topic = Topic.objects.get(id=id).annotate(
                tool_count=Count("tools")
                )
            self.check_object_permissions(self.request, topic)
            return topic
        except Topic.DoesNotExist:
            raise Http404

    def get(self, request, id):
        topic = self.get_object(id)
        serializer = TopicSerializer(
            topic, context={"request": request}
            )
        return Response(serializer.data)


class ToolsOfTopicBySlug(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ToolSerializer

    def get(self, request, slug):

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


class IconsList(APIView):

    def get(self, request):
        icons = Icon.objects.all()
        serializer = IconSerializer(icons, many=True)
        return Response(serializer.data)
