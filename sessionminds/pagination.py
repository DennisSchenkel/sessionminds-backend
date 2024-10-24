from rest_framework.pagination import PageNumberPagination


# Custom pagination class with page size set to 10
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
