from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from comments.models import Comment
from comments.serializers import CommentSerializer
from tools.models import Tool
from sessionminds.permissions import IsOwnerOrReadOnly


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
        serializer = CommentSerializer(comment, context={"request": request})
        return Response(serializer.data, status=201)


class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs["id"])

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
