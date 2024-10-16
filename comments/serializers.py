from rest_framework import serializers
from comments.models import Comment
from profiles.serializers import ProfileSerializer


# Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model

    Args:
        serializers.ModelSerializer: The base serializer class.
    """
    profile = ProfileSerializer(source="user.profile", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "tool", "user", "profile", "text", "created_at"]
