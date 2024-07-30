from rest_framework import serializers
from .models import Tool


class ToolSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the authenticated user is the owner of the object.

        Args:
            obj (object): The object to check ownership for.

        Returns:
            bool: True if the authenticated user is the owner, False otherwise.
        """
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user == obj.user

    class Meta:
        model = Tool
        fields = [
            "title",
            "short_description",
            "categories",
            ]