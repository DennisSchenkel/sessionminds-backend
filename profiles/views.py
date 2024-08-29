from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
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
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles, many=True, context={"request": request}
            )
        return Response(serializer.data)


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

    # Check if profile exists and return it or return 404
    # This method is only to validate the profile exists
    def get_object(self, id):
        try:
            profile = Profile.objects.get(id=id)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    # Get profile by id and return it
    # If profile does exist, return it so it can be used
    def get(self, request, id):
        """
        Retrieve a specific profile.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The primary key of the profile to retrieve.

        Returns:
            Response: The serialized profile data.
        """
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
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)


# Get a list of all users
class UsersListView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# Get a single user by user id
class UserDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

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
    def put(self, request, user_id):
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


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if request.user != user:
            return Response(
                {"You are not allowed to delete this profile!"},
                status=status.HTTP_403_FORBIDDEN
                )

        # Benutzer löschen
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Register new user
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializer.data,
            "user_id": user.id,
            "email": user.email
        }, status=status.HTTP_201_CREATED)


# Login user
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Create JWT Tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user_id": user.id,
            "email": user.email
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Blacklist the access token
        access_token = request.headers.get('Authorization', '').split(' ')[-1]
        if access_token:
            try:
                token = AccessToken(access_token)
                token.blacklist()
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                    )

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "You have access to this protected endpoint!"
        })
