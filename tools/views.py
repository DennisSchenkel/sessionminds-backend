from django.http import Http404
from django.db.models import Count
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from sessionminds.pagination import CustomPageNumberPagination
from .models import Tool
from .serializers import ToolSerializer
from sessionminds.permissions import IsOwnerOrReadOnly


# Get all tools
class ToolList(APIView):
    """
    A view for retrieving a list of tools.

    Inherits from APIView class.

    Methods:
        get(request):
            Retrieves all tools and returns serialized data.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ToolSerializer

    def get(self, request):

        ordering = request.query_params.get("ordering", "latest")

        if ordering == "votes":
            tools = Tool.objects.annotate(
                vote_count=Count("votes")
                ).order_by("-vote_count")
        else:
            tools = Tool.objects.all().order_by("-created")

        paginator = CustomPageNumberPagination()
        paginated_tools = paginator.paginate_queryset(tools, request)

        serializer = ToolSerializer(
            paginated_tools, many=True, context={"request": request}
            )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ToolSerializer(
            data=request.data,
            context={"request": request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToolDetailById(APIView):
    """
    A view for retrieving a single tool.

    Inherits from APIView class.

    Methods:
        get(request, id):
            Retrieves a single tool and returns serialized data.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ToolSerializer

    # Check if tool exists and return it or return 404
    # This method is only to validate the tool exists
    def get_object(self, id):
        try:
            tool = Tool.objects.get(id=id)
            self.check_object_permissions(self.request, tool)
            return tool
        except Tool.DoesNotExist:
            raise Http404

    # Get tool by id and return it
    # If tool does exist, return it so it can be used
    def get(self, request, id):
        tool = self.get_object(id)
        serializer = ToolSerializer(
            tool, context={"request": request}
            )
        return Response(serializer.data)

    # Update tool by id
    def put(self, request, id):
        tool = self.get_object(id)
        serializer = ToolSerializer(
            tool,
            data=request.data,
            context={"request": request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete tool by id
    def delete(self, request, id):
        tool = self.get_object(id)
        tool.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Get a single tool
class ToolDetailBySlug(APIView):
    """
    A view for retrieving a single tool.

    Inherits from APIView class.

    Methods:
        get(request, slug):
            Retrieves a single tool and returns serialized data.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ToolSerializer

    # Check if tool exists and return it or return 404
    # This method is only to validate the tool exists
    def get_object(self, slug):
        try:
            tool = Tool.objects.get(slug=slug)
            self.check_object_permissions(self.request, tool)
            return tool
        except Tool.DoesNotExist:
            raise Http404

    # Get tool by slug and return it
    # If tool does exist, return it so it can be used
    def get(self, request, slug):
        tool = self.get_object(slug)
        serializer = ToolSerializer(
            tool, context={"request": request}
            )
        return Response(serializer.data)

    # Update tool by slug
    def put(self, request, slug):
        tool = self.get_object(slug)
        serializer = ToolSerializer(
            tool,
            data=request.data,
            context={"request": request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete tool by slug
    def delete(self, request, slug):
        tool = self.get_object(slug)
        tool.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
