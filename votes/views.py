from rest_framework import permissions
from rest_framework import generics
from .models import Vote
from sessionminds.permissions import IsOwnerOrReadOnly
from .serializers import VoteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Get all votes
class VoteList(generics.ListCreateAPIView):
    """
    A view for retrieving a list of votes.

    Args:
        generics (ListCreateAPIView): Inherits from ListCreateAPIView class.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    # Create a new vote
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Get single vote by id
class VoteDetails(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a vote.

    Args:
        generics (RetrieveDestroyAPIView):
        Inherits from RetrieveDestroyAPIView class.

    Returns:
        VoteDetails: The vote details view.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()


# Get votes by tool
class VotesByTool(APIView):
    """
    A view to retrieve votes by tool.

    Args:
        APIView: Inherits from APIView class.

    Returns:
        VotesByTool: The votes by tool view.
    """
    permission_classes = [permissions.AllowAny]

    # Get votes by tool
    def get(self, request, *args, **kwargs):
        tool_id = kwargs.get("id")

        user_has_voted = False
        vote_id = None

        if request.user.is_authenticated:
            vote = Vote.objects.filter(tool=tool_id, user=request.user).first()
            if vote:
                user_has_voted = True
                vote_id = vote.id

        return Response({
            "user_has_voted": user_has_voted,
            "vote_id": vote_id
        })
