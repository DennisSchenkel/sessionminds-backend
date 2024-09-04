from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import models
from rest_framework import serializers
from .models import Profile
from tools.models import Tool


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    is_owner = serializers.SerializerMethodField()
    tool_count = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()

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
            raise serializers.ValidationError(
                "Image file is too large! ( max 2mb )"
                )
        if value.image.width < 300 or value.image.height < 300:
            raise serializers.ValidationError(
                "Image file is too small! ( min 300x300 pixels )"
                )
        if value.image.width > 4096 or value.image.height > 4096:
            raise serializers.ValidationError(
                "Image file is too large! ( max 4096x4096 pixels )"
                )
        if value.file.content_type not in ["image/jpeg", "image/png"]:
            raise serializers.ValidationError(
                "Image file is not a valid format! ( jpeg, png )"
                )

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
            "user_id",
            "is_owner",
            "tool_count",
            "total_votes",
            ]

    def get_tool_count(self, obj):
        return Tool.objects.filter(user=obj.user).count()

    def get_total_votes(self, obj):
        users_tools = Tool.objects.filter(user=obj.user)
        total_votes = users_tools.annotate(
            vote_count=models.Count('votes')).aggregate(
                total_votes=models.Sum('vote_count')
                )['total_votes']
        return int(total_votes) if total_votes is not None else 0


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            ]

    def update(self, instance, validated_data):
        email = validated_data.get("email", instance.email).lower()
        username = validated_data.get("username", instance.username).lower()
        instance.username = username
        instance.email = email
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
        )
    passwordConf = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "passwordConf")

    def validate(self, data):
        if data["password"] != data["passwordConf"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("passwordConf")
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"].lower(),
            password=validated_data["password"]
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email").lower()
        password = data.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"),
                                username=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    "Invalid credentials, please try again."
                    )
        else:
            raise serializers.ValidationError(
                "Both 'email' and 'password' are required."
                )

        data["user"] = user
        return data
