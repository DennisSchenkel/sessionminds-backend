from rest_framework import serializers
from comments.models import Comment
from profiles.serializers import ProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source="user.profile", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "tool", "user", "profile", "text", "created_at"]
