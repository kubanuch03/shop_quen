from rest_framework import pagination


class ListProductPagination(pagination.PageNumberPagination):
    page_size = 30