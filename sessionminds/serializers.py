from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CustomUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyFrield(source="profile.id")
    profile_image = serializers.ImageField(source="profile.image.url")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "profile_id", "profile_image"
            )