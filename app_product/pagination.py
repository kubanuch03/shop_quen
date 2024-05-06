
from rest_framework.pagination import PageNumberPagination

class ListProductPagination(PageNumberPagination):
    default_limit = 50
    page_size_query_param = 'page_size'
    max_limit = 10000

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        self.page_size = page_size  # Устанавливаем размер страницы для текущего запроса
        return super().paginate_queryset(queryset, request, view)
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 100
