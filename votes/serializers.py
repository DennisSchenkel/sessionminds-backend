from rest_framework import serializers
from django.db import IntegrityError
from .models import Vote


class VoteSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source="user.username")
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.user

    class Meta:
        model = Vote
        fields = "__all__"

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "It seems you have already voted for this tool."
            })
