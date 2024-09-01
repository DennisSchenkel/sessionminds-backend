from rest_framework import serializers
from .models import Tool
from categories.serializers import CategorySerializer
from profiles.serializers import ProfileSerializer


class ToolSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    is_owner = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True)
    profile = ProfileSerializer(source='user.profile', read_only=True)

    def get_is_owner(self, obj):
        """
        Check if the authenticated user is the owner of the tool.

        Args:
            obj (object): The object to check ownership for.

        Returns:
            bool: True if the authenticated user is the owner.
        """
        request = self.context["request"]
        return request.user == obj.user

    class Meta:
        model = Tool
        fields = [
            "id",
            "user",
            "profile",
            "title",
            "short_description",
            "full_description",
            "category",
            "instructions",
            "slug",
            "created",
            "updated",
            "is_owner",
            ]
