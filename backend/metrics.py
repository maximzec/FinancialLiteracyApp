from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.multiprocess import MultiProcessCollector
from prometheus_client.registry import REGISTRY
import time
from typing import Callable
from fastapi import Request, Response
import psutil
import os

# Метрики для HTTP запросов
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Метрики для бизнес-логики
user_registrations_total = Counter(
    'user_registrations_total',
    'Total number of user registrations'
)

lesson_completions_total = Counter(
    'lesson_completions_total',
    'Total number of lesson completions',
    ['lesson_id']
)

ai_requests_total = Counter(
    'ai_requests_total',
    'Total number of AI requests',
    ['request_type']
)

ai_request_duration_seconds = Histogram(
    'ai_request_duration_seconds',
    'AI request duration in seconds',
    ['request_type']
)

# Метрики системы
active_users = Gauge(
    'active_users',
    'Number of currently active users'
)

database_connections = Gauge(
    'database_connections_active',
    'Number of active database connections'
)

# Метрики ресурсов
cpu_usage_percent = Gauge(
    'cpu_usage_percent',
    'CPU usage percentage'
)

memory_usage_bytes = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes'
)

disk_usage_percent = Gauge(
    'disk_usage_percent',
    'Disk usage percentage'
)


class PrometheusMiddleware:
    """Middleware для сбора метрик HTTP запросов"""

    def __init__(self, app_name: str = "financial_literacy_app"):
        self.app_name = app_name

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Получаем путь без query параметров
        path = request.url.path
        method = request.method

        # Выполняем запрос
        response = await call_next(request)

        # Записываем метрики
        duration = time.time() - start_time
        status_code = str(response.status_code)

        http_requests_total.labels(
            method=method,
            endpoint=path,
            status_code=status_code
        ).inc()

        http_request_duration_seconds.labels(
            method=method,
            endpoint=path
        ).observe(duration)

        return response


def update_system_metrics():
    """Обновляет системные метрики"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_usage_percent.set(cpu_percent)

        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage_bytes.set(memory.used)

        # Disk usage
        disk = psutil.disk_usage('/')
        disk_usage_percent.set(disk.percent)

    except Exception as e:
        print(f"Error updating system metrics: {e}")


def get_metrics():
    """Возвращает метрики в формате Prometheus"""
    # Обновляем системные метрики
    update_system_metrics()

    # Если используется multiprocess mode
    if 'prometheus_multiproc_dir' in os.environ:
        registry = REGISTRY
        MultiProcessCollector(registry)

    return generate_latest()


# Декораторы для бизнес-метрик
def track_user_registration():
    """Декоратор для отслеживания регистраций пользователей"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            user_registrations_total.inc()
            return result
        return wrapper
    return decorator


def track_lesson_completion(lesson_id: str):
    """Декоратор для отслеживания завершения уроков"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            lesson_completions_total.labels(lesson_id=lesson_id).inc()
            return result
        return wrapper
    return decorator


def track_ai_request(request_type: str):
    """Декоратор для отслеживания AI запросов"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                ai_requests_total.labels(request_type=request_type).inc()
                return result
            finally:
                duration = time.time() - start_time
                ai_request_duration_seconds.labels(
                    request_type=request_type).observe(duration)
        return wrapper
    return decorator
