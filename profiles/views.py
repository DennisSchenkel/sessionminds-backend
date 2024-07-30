from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


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
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


# Get single profile by id
class ProfileDetail(APIView):
    """
    A view to retrieve a specific profile.

    This view allows to retrieve a profile by its ID.

    Methods:
        get_object(pk):
            Check if profile exists and return it or raise Http404.
        get(request, pk):
            Get profile by ID and return it.
    """
    serializer_class = ProfileSerializer

    # Check if profile exists and return it or return 404
    # This method is only to validate the profile exists
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    # Get profile by id and return it
    # If profile does exist, return it so it can be used
    def get(self, request, pk):
        """
        Retrieve a specific profile.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the profile to retrieve.

        Returns:
            Response: The serialized profile data.
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    # Update profile by id and save it
    def put(self, request, pk):
        """
        Update an existing profile.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the profile to be updated.

        Returns:
            Response: HTTP response object containing the updated profile data.

        Raises:
            NotFound: If the profile with the given primary key does not exist.
            ValidationError: If the request data is invalid.
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
