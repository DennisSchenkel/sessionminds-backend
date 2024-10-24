from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from PIL import Image
from .models import Profile


# Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    Args:
        serializers.ModelSerializer: The base serializer class.

    Raises:
        serializers.ValidationError: If the image file is too large, too small,
        not a valid image format, or not a valid image file.

    Returns:
        ProfileSerializer: The serialized Profile object.
    """
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

    # Custom validation for the image field
    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError(
                "Image file is too large! ( max 2MB )"
                )
        try:
            img = Image.open(value)
            width, height = img.size
            img_format = img.format
        except Exception:
            raise serializers.ValidationError(
                "Uploaded file is not a valid image."
                )

        # Reset the file pointer to the beginning of the file
        value.seek(0)

        if width < 300 or height < 300:
            raise serializers.ValidationError(
                "Image file is too small! ( min 300x300 pixels )"
                )
        if width > 4096 or height > 4096:
            raise serializers.ValidationError(
                "Image file is too large! ( max 4096x4096 pixels )"
                )
        if img_format not in ["JPEG", "PNG"]:
            raise serializers.ValidationError(
                "Image file is not a valid format! (jpeg, png)"
                )

        return value

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "user_id",
            "first_name",
            "last_name",
            "job_title",
            "profile_description",
            "linkedin",
            "twitter",
            "facebook",
            "instagram",
            "image",
            "tool_count",
            "total_votes",
            "slug",
            "created",
            "updated",
            "is_owner",
            ]

    # Access the annotated value in the queryset for tool count
    def get_tool_count(self, obj):
        return getattr(obj, "annotated_tool_count", 0)

    # Access the annotated value in the queryset for total votes
    def get_total_votes(self, obj):
        return getattr(obj, "annotated_total_votes", 0)


# User serializer
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Args:
        serializers.ModelSerializer: The base serializer class.

    Returns:
        UserSerializer: The serialized User object.
    """
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

    # Override the update method to handle email and username
    def update(self, instance, validated_data):
        """
        Update the user's email and username.

        Args:
            instance (object): The User object to update.
            validated_data (dict): The validated data to update the User object

        Returns:
            User: The updated User object.
        """
        email = validated_data.get("email", instance.email).lower()
        username = validated_data.get("username", instance.username).lower()
        instance.username = username
        instance.email = email
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance


# Registration serializer
class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for the registration of a new user.

    Args:
        serializers.ModelSerializer: The base serializer class

    Raises:
        serializers.ValidationError: If the passwords do not match

    Returns:
        RegistrationSerializer: The serialized User object.
    """
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="You are already registered with this email."
            )
        ]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )
    passwordConf = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("email", "password", "passwordConf")

    # Validate the email field
    def validate_email(self, value):
        return value.lower()

    # Validate the password fields
    def validate(self, data):
        if data["password"] != data["passwordConf"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    # Create a new user
    def create(self, validated_data):
        validated_data.pop("passwordConf")
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"].lower(),
            password=validated_data["password"]
        )
        return user


# Login serializer
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Args:
        serializers.Serializer: The base serializer class.

    Raises:
        serializers.ValidationError: If the credentials are invalid.

    Returns:
        LoginSerializer: The serialized User object.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # Validate the email and password fields
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
