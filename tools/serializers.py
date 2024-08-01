from rest_framework import serializers
from .models import Tool


class ToolSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the authenticated user is the owner of the tool.

        Args:
            obj (object): The object to check ownership for.

        Returns:
            bool: True if the authenticated user is the owner.
        """
        request = self.context["request"]
        return request.user == obj.owner

    class Meta:
        model = Tool
        fields = [
            "id",
            "owner",
            "title",
            "short_description",
            "full_description",
            "categories",
            "instructions",
            "slug",
            "created",
            "updated",
            "is_owner",
            ]
