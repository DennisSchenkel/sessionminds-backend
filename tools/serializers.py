from rest_framework import serializers
from .models import Tool
from topics.models import Topic
from topics.serializers import TopicSerializer
from profiles.serializers import ProfileSerializer


class ToolSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source="user.username")
    profile = ProfileSerializer(source="user.profile", read_only=True)

    # Write-only field for accepting topic IDs on create/update
    topic_ids = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), many=True, write_only=True
    )

    # Read-only field to include full topic details in the response
    topics = TopicSerializer(many=True, read_only=True)

    vote_count = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.user

    def get_vote_count(self, obj):
        return obj.votes.count()

    # Override the create method to handle topic_ids field
    def create(self, validated_data):
        topic_ids = validated_data.pop('topic_ids')
        tool = Tool.objects.create(**validated_data)
        tool.topics.set(topic_ids)  # Set the related topics
        return tool

    # Override the update method to handle topic_ids field
    def update(self, instance, validated_data):
        topic_ids = validated_data.pop('topic_ids', None)
        instance = super().update(instance, validated_data)
        if topic_ids is not None:
            instance.topics.set(topic_ids)
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
            "topics",
            "topic_ids",
            "profile",
            "icon",
            "slug",
            "created",
            "updated",
            "is_owner",
            "vote_count",
        ]
