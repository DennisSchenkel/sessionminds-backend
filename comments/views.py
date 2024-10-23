from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from comments.models import Comment
from comments.serializers import CommentSerializer
from tools.models import Tool
from profiles.models import Profile
from sessionminds.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView


# Get all comments for a tool or create a new comment
class ToolComments(generics.ListCreateAPIView):
    """
    Retrieve all comments for a tool or create a new comment.

    Args:
        generics (ListCreateAPIView): Inherits from ListCreateAPIView class.

    Returns:
        ToolComments: The tool comments view.
    """
    serializer_class = CommentSerializer

    def get_permissions(self):
        """
        Override get_permissions to apply different permissions
        based on the request method.
        """
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        tool_id = self.kwargs.get("id")
        tool = get_object_or_404(Tool, id=tool_id)
        return Comment.objects.filter(tool=tool).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        """
        Create a new comment.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The serialized comment data.
        """
        user = request.user

        try:
            profile = user.profile
            if not (profile.first_name and profile.last_name):
                return Response(
                    {"detail": "You need first and last names to comment."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        tool = get_object_or_404(Tool, id=self.kwargs["id"])
        text = request.data.get("text", "").strip()

        if not text:
            return Response(
                {"detail": "Comment text cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        comment = Comment(tool=tool, user=user, text=text)
        comment.save()
        serializer = CommentSerializer(comment, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Get single comment by id
class CommentDetails(APIView):
    """
    Retrieve, update, or delete a comment.

    Args:
        APIView: Inherits from APIView class.

    Returns:
        CommentDetails: The comment details view.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_object(self, id):
        """
        Get a single comment by id and check object permissions.

        Args:
            id (int): The comment id.

        Returns:
            Comment: The comment object.
        """
        comment = get_object_or_404(Comment, id=id)
        self.check_object_permissions(self.request, comment)
        return comment

    def get(self, request, id):
        """
        Retrieve a single comment.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The comment id.

        Returns:
            Response: The serialized comment data.
        """
        comment = self.get_object(id)
        serializer = CommentSerializer(comment, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, id):
        """
        Delete a single comment.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The comment id.

        Returns:
            Response: Status 204 on successful deletion.
        """
        comment = self.get_object(id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
