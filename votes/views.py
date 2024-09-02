from rest_framework import permissions
from rest_framework import generics
from .models import Vote
from sessionminds.permissions import IsOwnerOrReadOnly
from .serializers import VoteSerializer


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
