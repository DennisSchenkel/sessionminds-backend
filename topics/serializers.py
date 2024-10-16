from rest_framework import serializers
from .models import Topic, Icon


class IconSerializer(serializers.ModelSerializer):
    """
    Serializer for the Icon model.

    Args:
        serializers.ModelSerializer: The base serializer class.
    """

    class Meta:
        model = Icon
        fields = [
            "id",
            "title",
            "icon_code",
            ]


class TopicSerializer(serializers.ModelSerializer):
    """
    Serializer for the Topic model.

    Args:
        serializers.ModelSerializer: The base serializer class.

    Returns:
        TopicSerializer: The serialized Topic object.
    """
    icon = IconSerializer(read_only=True)
    tool_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "tool_count",
            "icon",
            ]

    # Get the number of tools associated with the topic
    def get_tool_count(self, obj):
        return obj.tools.count()
