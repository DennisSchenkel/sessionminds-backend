from rest_framework import serializers
from django.db import IntegrityError
from .models import Vote


# Vote serializer
class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vote model.

    Args:
        serializers.ModelSerializer: The base serializer class.

    Raises:
        serializers.ValidationError:
        If the user has already voted for the tool.

    Returns:
        VoteSerializer: The serialized Vote object.
    """
    user = serializers.ReadOnlyField(source="user.username")
    is_owner = serializers.SerializerMethodField()

    # Check if the user is the owner of the vote
    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.user

    class Meta:
        model = Vote
        fields = "__all__"

    # Override the create method to handle IntegrityError
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "It seems you have already voted for this tool."
            })
