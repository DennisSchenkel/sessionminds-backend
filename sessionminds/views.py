from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def root_route(request):
    return Response({
        "Welcome to the SessionMinds API. For more information, visit "
        "the documentation at: "
        "https://github.com/DennisSchenkel/sessionminds-frontend"
    })
