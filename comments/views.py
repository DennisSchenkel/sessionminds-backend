from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from comments.models import Comment
from comments.serializers import CommentSerializer
from tools.models import Tool


class ToolComments(generics.ListCreateAPIView):
    """
    List all comments for a tool or create a new comment.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        tool = get_object_or_404(Tool, id=self.kwargs["id"])
        return tool.comments.all()

    def create(self, request, *args, **kwargs):
        tool = get_object_or_404(Tool, id=self.kwargs["id"])
        comment = Comment(
            tool=tool, user=request.user, text=request.data["text"]
            )
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
