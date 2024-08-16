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

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ToolSerializer

    def get(self, request):
        tools = Tool.objects.all()
        serializer = ToolSerializer(
            tools, many=True, context={'request': request}
            )
        return Response(serializer.data)

    def post(self, request):
        serializer = ToolSerializer(
            data=request.data,
            context={"request": request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get a single tool
class ToolDetail(APIView):
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
