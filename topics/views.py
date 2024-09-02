from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .serializers import TopicSerializer, IconSerializer
from .models import Topic, Icon


# Get all categories
class TopicsList(APIView):
    """
    A view for retrieving a list of categories.

    Inherits from APIView class.

    Methods:
        get(request): Retrieves all categories and returns serialized data.
    """
    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


# Get single category by slug
class TopicDetail(APIView):
    """
    A view to retrieve a specific category.

    This view allows to retrieve a category by its slug.

    Methods:
        get_object(slug):
            Check if category exists and return it or raise Http404.
        get(request, slug):
            Get category by slug and return it.
    """
    serializer_class = TopicSerializer

    # Check if category exists and return it or return 404
    # This method is only to validate the category exists
    def get_object(self, slug):
        try:
            topic = Topic.objects.get(slug=slug)
            self.check_object_permissions(self.request, topic)
            return topic
        except Topic.DoesNotExist:
            raise Http404

    # Get category by slug and return it
    # If category does exist, return it so it can be used
    def get(self, request, slug):
        """
        Retrieve a specific category.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The primary key of the category to retrieve.

        Returns:
            Response: The serialized category data.
        """
        topic = self.get_object(slug)
        serializer = TopicSerializer(
            topic, context={"request": request}
            )
        return Response(serializer.data)


class TopicDetailById(APIView):
    serializer_class = TopicSerializer

    def get_object(self, id):
        try:
            topic = Topic.objects.get(id=id)
            self.check_object_permissions(self.request, topic)
            return topic
        except Topic.DoesNotExist:
            raise Http404

    def get(self, request, id):
        topic = self.get_object(id)
        serializer = TopicSerializer(
            topic, context={"request": request}
            )
        return Response(serializer.data)


class IconsList(APIView):

    def get(self, request):
        icons = Icon.objects.all()
        serializer = IconSerializer(icons, many=True)
        return Response(serializer.data)
