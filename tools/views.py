from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
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
    def get(self, request):
        tools = Tool.objects.all()
        serializer = ToolSerializer(
            tools, many=True, context={'request': request}
            )
        return Response(serializer.data)


# Get a single tool
class ToolDetail(APIView):
    """
    A view for retrieving a single tool.

    Inherits from APIView class.

    Methods:
        get(request, slug):
            Retrieves a single tool and returns serialized data.
    """

    def get_object(self, slug):
        try:
            tool = Tool.objects.get(slug=slug)
            self.check_object_permissions(self.request, tool)
            return tool
        except Tool.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        tool = self.get_object(slug)
        serializer = ToolSerializer(
            tool, context={"request": request}
            )
        return Response(serializer.data)


class ToolCreate(APIView):
    """
    A view for creating a tool.

    Inherits from APIView class.

    Methods:
        get(request):
            Retrieve the serialized data for creating a new tool.

        post(request):
            Create a new tool and return serialized data.

    Attributes:
        permission_classes (list): A list of permission classes for the view.
        serializer_class (class): The serializer class for the view.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ToolSerializer

    def post(self, request):
        serializer = ToolSerializer(
            data=request.data,
            context={"request": request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToolUpdate(APIView):
    """
    Update a tool and return serialized data.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the tool to be updated.

    Returns:
        Response:
            The HTTP response object containing
            the serialized data of the updated tool.

    Raises:
        Tool.DoesNotExist:
            If the tool with the given ID does not exist.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ToolSerializer

    def get_object(self, id):
        try:
            tool = Tool.objects.get(id=id)
            self.check_object_permissions(self.request, tool)
            return tool
        except Tool.DoesNotExist:
            raise Http404

    def put(self, request, id):
        tool = self.get_object(id)
        serializer = ToolSerializer(
            tool,
            data=request.data,
            context={"request": request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
