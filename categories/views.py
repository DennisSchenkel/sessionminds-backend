from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .serializers import CategorySerializer
from .models import Category, Icon


# Get all categories
class CategoriesList(APIView):
    """
    A view for retrieving a list of categories.

    Inherits from APIView class.

    Methods:
        get(request): Retrieves all categories and returns serialized data.
    """
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# Get single category by id
class CategoryDetail(APIView):
    """
    A view to retrieve a specific category.

    This view allows to retrieve a category by its ID.

    Methods:
        get_object(id):
            Check if category exists and return it or raise Http404.
        get(request, id):
            Get category by ID and return it.
    """
    serializer_class = CategorySerializer

    # Check if category exists and return it or return 404
    # This method is only to validate the category exists
    def get_object(self, id):
        try:
            category = Category.objects.get(id=id)
            self.check_object_permissions(self.request, category)
            return category
        except Category.DoesNotExist:
            raise Http404

    # Get category by id and return it
    # If category does exist, return it so it can be used
    def get(self, request, id):
        """
        Retrieve a specific category.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The primary key of the category to retrieve.

        Returns:
            Response: The serialized category data.
        """
        category = self.get_object(id)
        serializer = CategorySerializer(
            category, context={'request': request}
            )
        return Response(serializer.data)


class IconsList(APIView):
    """
    A view for retrieving a list of icons.

    Inherits from APIView class.

    Methods:
        get(request): Retrieves all icons and returns serialized data.
    """
    def get(self, request):
        icons = Icon.objects.all()
        return Response(icons)
