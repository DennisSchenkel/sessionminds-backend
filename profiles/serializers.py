from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
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
        request = self.context["request"]
        return request.user == obj.user

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image file is too large! ( max 2mb )")
        if value.image.width < 300 or value.image.height < 300:
            raise serializers.ValidationError("Image file is too small! ( min 300x300 pixels )")
        if value.image.width > 4096 or value.image.height > 4096:
            raise serializers.ValidationError("Image file is too large! ( max 4096x4096 pixels )")
        if value.file.content_type not in ["image/jpeg", "image/png"]:
            raise serializers.ValidationError("Image file is not a valid format! ( jpeg, png )")
        

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "profile_description",
            "linkedin",
            "image",
            "created",
            "updated",
            "is_owner",
            ]
