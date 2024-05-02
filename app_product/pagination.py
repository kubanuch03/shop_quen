
from rest_framework.pagination import PageNumberPagination

class ListProductPagination(PageNumberPagination):
    default_limit = 50
    # page_size_query_param = 'page_size'
    max_limit = 100