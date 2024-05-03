from celery import shared_task
from django.core.cache import cache
from .models import Product
from .serializer import ProductListSerializer
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from .pagination import ListProductPagination
from django.utils import timezone
from django.http.request import HttpRequest


logger = get_task_logger(__name__)



@shared_task
def clear_cache():
    logger.info('Очищаем кеш...')
    cache.clear()
    logger.info('Очищено')



@shared_task
def check_cache_expiry():
    products_in_cache = cache.keys('product_*')  # Получаем все ключи товаров из кеша
    for key in products_in_cache:
        product_id = key.split('_')[1]
        product = Product.objects.get(id=product_id)  # Получаем товар из базы данных
        time_since_last_request = datetime.now() - product.last_requested_at
        if time_since_last_request > timedelta(days=30):  # Проверяем время жизни
            cache.delete(key) 

def add_product_to_cache(product_id):
    product = Product.objects.get(id=product_id)
    cache.set(f'product_{product_id}', product, timeout=None) 
    cached_products = cache.get('cached_products', [])
    cached_products.append(product_id)
    cache.set('cached_products', cached_products, timeout=None) 


# Можно также обновлять время последнего запроса при каждом запросе к товару
def update_last_requested_time(product_id):
    product = Product.objects.get(id=product_id)
    product.last_requested_at = datetime.now()
    product.save()


@shared_task
def update_product_cache(page_number, page_size, query_params):
    try:
        queryset = Product.objects.all().select_related('subcategory').prefetch_related('characteristics', 'color', 'size').order_by('-id')
        paginator = ListProductPagination()
        # Construct a fake request object with the query parameters
        fake_request = HttpRequest(query_params)
        paginated_queryset = paginator.paginate_queryset(queryset, fake_request)
        serializer = ProductListSerializer(paginated_queryset, many=True)
        serialized_data = serializer.data

        # Кешируем результаты на 10 секунд
        cache.set(f'cached_products_page_{page_number}', serialized_data, timeout=30)
        logger.info(f"Товары страницы {page_number} успешно закешированы")
    except Exception as e:
        logger.error(f"Ошибка кеширования товаров страницы {page_number}: {str(e)}")