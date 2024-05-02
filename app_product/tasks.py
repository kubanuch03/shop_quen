from celery import shared_task
from django.core.cache import cache
from .models import Product
from .serializer import ProductListSerializer
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def update_product_cache():
    try:
        queryset = Product.objects.all().select_related('subcategory').prefetch_related('characteristics', 'color', 'size').order_by('-id')
        serializer = ProductListSerializer(queryset, many=True)
        serialized_data = serializer.data

        # Кешируем результаты на 10 секунд
        cache.set('cached_products', serialized_data, timeout=10)
        logger.info("Товары успешно закешированы")
    except Exception as e:
        logger.error(f"Ошибка кеширования товаров: {str(e)}")
        