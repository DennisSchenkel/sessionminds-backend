from rest_framework import serializers
from .models import Topic, Icon


class IconSerializer(serializers.ModelSerializer):

    class Meta:
        model = Icon
        fields = [
            "id",
            "title",
            "icon_code",
            ]


class TopicSerializer(serializers.ModelSerializer):
    icon = IconSerializer(read_only=True)
    tool_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "slug",
            "tool_count",
            ]

    def get_tool_count(self, obj):
        return obj.tools.count()
