from rest_framework import serializers
from .models import Tool
from topics.models import Topic
from topics.serializers import TopicSerializer
from profiles.serializers import ProfileSerializer
from comments.serializers import CommentSerializer


class ToolSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tool model.

    Args:
        serializers.ModelSerializer: The base serializer class.

    Returns:
        ToolSerializer: The serialized Tool object.
    """
    is_owner = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source="user.username")
    profile = ProfileSerializer(source="user.profile", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    # Write-only field for accepting topic IDs on create/update
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(),
        write_only=True,
        required=False,
        default=1
    )

    # Read-only field to include full topic details in the response
    topic = TopicSerializer(read_only=True)

    vote_count = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.user

    def get_vote_count(self, obj):
        return obj.votes.count()

    # Override the create method to handle topic_ids field
    def create(self, validated_data):
        topic = validated_data.pop("topic_id", None)
        user = self.context["request"].user
        tool = Tool.objects.create(user=user, **validated_data)
        if topic:
            tool.topic = topic
            tool.save()
        return tool

    # Override the update method to handle topic_ids field
    def update(self, instance, validated_data):
        topic = validated_data.pop("topic_id", None)
        instance = super().update(instance, validated_data)
        if topic is not None:
            instance.topic = topic
            instance.save()
        return instance

    class Meta:
        model = Tool
        fields = [
            "id",
            "user",
            "title",
            "short_description",
            "full_description",
            "instructions",
            "topic",
            "topic_id",
            "profile",
            "icon",
            "slug",
            "created",
            "updated",
            "is_owner",
            "vote_count",
            "comments",
        ]
