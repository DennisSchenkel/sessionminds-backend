from .models import Tool
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ToolSerializer


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
    def get(self, request, slug):
        tool = Tool.objects.get(slug=slug)
        serializer = ToolSerializer(
            tool, context={'request': request}
            )
        return Response(serializer.data)
