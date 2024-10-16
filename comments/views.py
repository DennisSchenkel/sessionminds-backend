from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from comments.models import Comment
from comments.serializers import CommentSerializer
from tools.models import Tool
from sessionminds.permissions import IsOwnerOrReadOnly


# Get all comments for a tool or create a new comment
class ToolComments(generics.ListCreateAPIView):
    """
    Retrieve all comments for a tool or create a new comment.

    Args:
        generics (ListCreateAPIView): Inherits from ListCreateAPIView class.

    Returns:
        ToolComments: The tool comments view.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    # Get all comments for a tool
    def get_queryset(self):
        tool = get_object_or_404(Tool, id=self.kwargs["id"])
        return tool.comments.all()

    # Create a new comment
    def create(self, request, *args, **kwargs):
        """
        Create a new comment.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The serialized comment data.
        """
        tool = get_object_or_404(Tool, id=self.kwargs["id"])
        comment = Comment(
            tool=tool, user=request.user, text=request.data["text"]
        )
        comment.save()
        serializer = CommentSerializer(comment, context={"request": request})
        return Response(serializer.data, status=201)


# Get single comment by id
class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve or delete a comment.

    Args:
        generics (RetrieveUpdateDestroyAPIView):
        Inherits from RetrieveUpdateDestroyAPIView class.

    Returns:
        CommentDetails: The comment details view.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    # Check if comment exists and return it or return 404
    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs["id"])

    # Update a comment
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
