from rest_framework import permissions
from rest_framework import generics
from .models import Vote
from sessionminds.permissions import IsOwnerOrReadOnly
from .serializers import VoteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class VoteList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VoteDetails(generics.RetrieveDestroyAPIView):

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()


class VotesByTool(APIView):
    permission_classes = [permissions.AllowAny]

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
