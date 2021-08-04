from rest_framework.pagination import PageNumberPagination


class SwiftPagination(PageNumberPagination):
    page_size_query_param = "size"
    page_size = 10
