from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from sessionminds.pagination import CustomPageNumberPagination
from django.db import IntegrityError
from .models import Profile
from .serializers import (
    ProfileSerializer,
    UserSerializer,
    RegistrationSerializer,
    LoginSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from sessionminds.permissions import IsOwnerOrReadOnly


# Get all profiles
class ProfileList(APIView):
    """
    A view for retrieving a list of profiles.

    Inherits from APIView class.

    Methods:
        get(request): Retrieves all profiles and returns serialized data.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    # Get all profiles
    def get(self, request):
        ordering = self.request.query_params.get("ordering", "tools")

        if ordering == "tools":
            profiles = Profile.objects.all().order_by("-tool_count")
        else:
            profiles = Profile.objects.all().order_by("-total_votes")

        paginator = CustomPageNumberPagination()
        paginated_profiles = paginator.paginate_queryset(profiles, request)

        serializer = ProfileSerializer(
            paginated_profiles, many=True, context={"request": request}
            )
        return paginator.get_paginated_response(serializer.data)


# Get single profile by profile id
class ProfileDetail(APIView):
    """
    A view to retrieve a specific profile.

    This view allows to retrieve a profile by its ID.

    Methods:
        get_object(id):
            Check if profile exists and return it or raise Http404.
        get(request, id):
            Get profile by ID and return it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    # Check if profile exists and return it or return 404
    # This method is only to validate the profile exists
    def get_object(self, id):
        """
        Check if a profile exists and return it or raise Http404.

        Args:
            id (int): The primary key of the profile to retrieve.

        Raises:
            Http404: If the profile with the given primary key does not exist.

        Returns:
            Profile: The profile object.
        """
        try:
            profile = Profile.objects.get(id=id)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    # Get profile by id and return it
    # If profile does exist, return it so it can be used
    def get(self, request, id):
        profile = self.get_object(id)
        serializer = ProfileSerializer(
            profile, context={"request": request})
        return Response(serializer.data)

    # Update profile by id and save it
    def put(self, request, id):
        """
        Update an existing profile.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The primary key of the profile to be updated.

        Returns:
            Response: HTTP response object containing the updated profile data.

        Raises:
            NotFound: If the profile with the given primary key does not exist.
            ValidationError: If the request data is invalid.
        """
        profile = self.get_object(id)
        serializer = ProfileSerializer(
            profile, data=request.data, context={"request": request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete profile by id
    def delete(self, request, id):
        """
        Delete an existing profile.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The primary key of the profile to be deleted.

        Returns:
            Response: HTTP response object indicating the profile was deleted.

        Raises:
            NotFound: If the profile with the given primary key does not exist.
        """
        profile = self.get_object(id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Get single profile by user id
class UserProfileView(APIView):
    """
    A view to retrieve a specific profile by user ID.

    Args:
        APIView: Inherits from APIView class.

    Returns:
        UserProfileView: The view to retrieve a specific profile by user ID.
    """
    permission_classes = [IsOwnerOrReadOnly]

    # Get profile by user id
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)

    # Update profile by user id
    def put(self, request, id):
        """
        Update an existing profile by user ID.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The primary key of the user to update the profile for.

        Returns:
            Response: The updated profile data.
        """
        user = get_object_or_404(User, id=id)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(
            profile, data=request.data, context={"request": request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get single profile by user slug
class UserProfileViewSlug(APIView):
    """
    A view to retrieve a specific profile by user slug.

    Args:
        APIView: Inherits from APIView class.
    """

    # Get profile by user slug
    def get(self, request, slug):
        """
        Retrieve a specific profile by user slug.

        Args:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug of the user to retrieve the profile for.

        Returns:
            Response: The serialized profile data.
        """
        profile = get_object_or_404(Profile, slug=slug)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)


# Get a list of all users
class UsersListView(APIView):
    """
    A view to retrieve a list of users

    Args:
        APIView: Inherits from APIView class.

    Returns:
        UsersListView: The view to retrieve a list of users.
    """
    permission_classes = [IsOwnerOrReadOnly]

    # Get all users
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# Get a single user by user id
class UserDetailView(APIView):
    """
    A view to retrieve a specific user by user ID.

    Args:
        APIView: Inherits from APIView class.

    Returns:
        UserDetailView: The view to retrieve a specific user by user ID.
    """
    permission_classes = [IsOwnerOrReadOnly]

    # Get a single user by user id
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
                )

        serializer = UserSerializer(user)
        return Response(serializer.data)


# Update user account
class UserUpdateView(APIView):
    """
    A view to update a user account.

    Args:
        APIView: Inherits from APIView class.

    Returns:
        UserUpdateView: The view to update a user account.
    """
    permission_classes = [IsOwnerOrReadOnly]

    # Update user account
    def put(self, request, user_id):
        """
        Update a user account.

        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The primary key of the user to update.

        Returns:
            Response: The updated user data.
        """
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if "email" in serializer.validated_data:
                serializer.validated_data["email"] = serializer.validated_data[
                    "email"
                    ].lower()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete user account
class UserDeleteView(APIView):
    """
    A view to delete a user account

    Args:
        APIView: Inherits from APIView class.

    Returns:
        UserDeleteView: The view to delete a user account.
    """
    permission_classes = [IsOwnerOrReadOnly]

    # Delete user account
    def delete(self, request, id):
        """
        Delete a user account.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The primary key of the user to delete.

        Returns:
            Response: A 204 response indicating the user was deleted.
        """
        user = get_object_or_404(User, id=id)

        if request.user != user:
            return Response(
                {"You are not allowed to delete this profile!"},
                status=status.HTTP_403_FORBIDDEN
                )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Register new user
class RegistrationView(generics.CreateAPIView):
    """
    A view to register a new user.

    Args:
        generics (CreateAPIView): Inherits from CreateAPIView class.

    Returns:
        RegistrationView: The view to register a new user.
    """
    serializer_class = RegistrationSerializer

    # Create a new user
    def create(self, request, *args, **kwargs):
        """
        Create a new user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The new user data.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "user_id": user.id,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"non_field_errors": [
                    "A user with this email already exists."
                    ]},
                status=status.HTTP_400_BAD_REQUEST
            )


# Login user
class LoginView(generics.GenericAPIView):
    """
    A view to login a user.

    Args:
        generics (GenericAPIView): Inherits from GenericAPIView class.

    Returns:
        LoginView: The view to login a user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    # Login user
    def post(self, request, *args, **kwargs):
        """
        Login a user.

        Args:
            request (HttpRequest): The HTTP request object

        Returns:
            Response: The JWT tokens for the user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Create JWT Tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "access": access_token,
            "refresh": refresh_token,
            "user_id": user.id,
            "email": user.email
        }, status=status.HTTP_200_OK)


# Logout user
class LogoutView(APIView):
    """
    A view to logout a user.

    Args:
        APIView: Inherits from APIView class.

    Returns:
        LogoutView: The view to logout a user.
    """
    permission_classes = [IsAuthenticated]

    # Logout user
    def post(self, request, *args, **kwargs):
        """
        Logout a user and blacklist the refresh token.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A message indicating the user was logged out.
        """
        # Blacklist the refresh token
        refresh_token = request.data.get("refreshToken")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )


# Protected view for testing token expiration
class ProtectedView(APIView):
    """
    A protected view for testing token expiration.

    Args:
        APIView: Inherits from APIView class.

    Returns:
        ProtectedView: The protected view for testing token expiration.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Get protected view
    def get(self, request):
        return Response({
            "message": "You have access to this protected endpoint!"
        })
