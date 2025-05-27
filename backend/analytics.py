from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import asyncio
import json
from clickhouse_driver import Client
from clickhouse_driver.errors import Error as ClickHouseError
import structlog
from pydantic import BaseModel
from enum import Enum

logger = structlog.get_logger()


class EventType(str, Enum):
    """Типы событий для аналитики"""
    USER_REGISTRATION = "user_registration"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    LESSON_START = "lesson_start"
    LESSON_COMPLETE = "lesson_complete"
    LESSON_PROGRESS = "lesson_progress"
    QUIZ_START = "quiz_start"
    QUIZ_COMPLETE = "quiz_complete"
    QUIZ_ANSWER = "quiz_answer"
    AI_CHAT_START = "ai_chat_start"
    AI_CHAT_MESSAGE = "ai_chat_message"
    SEARCH_QUERY = "search_query"
    PAGE_VIEW = "page_view"
    BUTTON_CLICK = "button_click"
    ERROR_OCCURRED = "error_occurred"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    COURSE_ENROLLMENT = "course_enrollment"
    PAYMENT_INITIATED = "payment_initiated"
    PAYMENT_COMPLETED = "payment_completed"


class AnalyticsEvent(BaseModel):
    """Модель события для аналитики"""
    event_id: str
    event_type: EventType
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: datetime
    properties: Dict[str, Any] = {}
    user_properties: Dict[str, Any] = {}
    device_info: Dict[str, Any] = {}
    location_info: Dict[str, Any] = {}


class ClickHouseAnalytics:
    """Класс для работы с ClickHouse аналитикой"""

    def __init__(self, host: str = "localhost", port: int = 9000, database: str = "analytics"):
        self.host = host
        self.port = port
        self.database = database
        self.client = None
        self._initialized = False

    async def initialize(self):
        """Инициализация подключения к ClickHouse"""
        try:
            self.client = Client(
                host=self.host,
                port=self.port,
                database=self.database
            )
            await self._create_tables()
            self._initialized = True
            logger.info("ClickHouse analytics initialized",
                        host=self.host, database=self.database)
        except Exception as e:
            logger.error("Failed to initialize ClickHouse", error=str(e))
            raise

    async def _create_tables(self):
        """Создание таблиц для аналитики"""

        # Основная таблица событий
        events_table = """
        CREATE TABLE IF NOT EXISTS events (
            event_id String,
            event_type String,
            user_id Nullable(String),
            session_id Nullable(String),
            timestamp DateTime64(3),
            properties String,
            user_properties String,
            device_info String,
            location_info String,
            date Date MATERIALIZED toDate(timestamp)
        ) ENGINE = MergeTree()
        PARTITION BY toYYYYMM(timestamp)
        ORDER BY (event_type, timestamp, user_id)
        SETTINGS index_granularity = 8192
        """

        # Таблица пользователей
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id String,
            registration_date DateTime64(3),
            last_activity DateTime64(3),
            total_lessons_completed UInt32,
            total_time_spent UInt64,
            subscription_type String,
            user_properties String,
            created_at DateTime64(3) DEFAULT now(),
            updated_at DateTime64(3) DEFAULT now()
        ) ENGINE = ReplacingMergeTree(updated_at)
        ORDER BY user_id
        """

        # Таблица сессий
        sessions_table = """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id String,
            user_id Nullable(String),
            start_time DateTime64(3),
            end_time Nullable(DateTime64(3)),
            duration_seconds Nullable(UInt64),
            page_views UInt32,
            events_count UInt32,
            device_info String,
            location_info String,
            referrer Nullable(String)
        ) ENGINE = ReplacingMergeTree(end_time)
        ORDER BY (session_id, start_time)
        """

        # Таблица уроков
        lessons_analytics_table = """
        CREATE TABLE IF NOT EXISTS lessons_analytics (
            lesson_id String,
            user_id String,
            started_at DateTime64(3),
            completed_at Nullable(DateTime64(3)),
            duration_seconds Nullable(UInt64),
            progress_percent UInt8,
            quiz_score Nullable(Float32),
            attempts_count UInt32,
            is_completed Bool
        ) ENGINE = ReplacingMergeTree(completed_at)
        ORDER BY (lesson_id, user_id, started_at)
        """

        # Материализованные представления для агрегации
        daily_stats_view = """
        CREATE MATERIALIZED VIEW IF NOT EXISTS daily_stats
        ENGINE = SummingMergeTree()
        ORDER BY (date, event_type)
        AS SELECT
            toDate(timestamp) as date,
            event_type,
            count() as events_count,
            uniq(user_id) as unique_users,
            uniq(session_id) as unique_sessions
        FROM events
        GROUP BY date, event_type
        """

        hourly_stats_view = """
        CREATE MATERIALIZED VIEW IF NOT EXISTS hourly_stats
        ENGINE = SummingMergeTree()
        ORDER BY (hour, event_type)
        AS SELECT
            toStartOfHour(timestamp) as hour,
            event_type,
            count() as events_count,
            uniq(user_id) as unique_users
        FROM events
        GROUP BY hour, event_type
        """

        tables = [
            events_table,
            users_table,
            sessions_table,
            lessons_analytics_table,
            daily_stats_view,
            hourly_stats_view
        ]

        for table_sql in tables:
            try:
                self.client.execute(table_sql)
                logger.info("Table created successfully")
            except ClickHouseError as e:
                logger.error("Failed to create table",
                             error=str(e), sql=table_sql)
                raise

    async def track_event(self, event: AnalyticsEvent):
        """Отправка события в аналитику"""
        if not self._initialized:
            logger.warning("Analytics not initialized, skipping event")
            return

        try:
            data = {
                'event_id': event.event_id,
                'event_type': event.event_type.value,
                'user_id': event.user_id,
                'session_id': event.session_id,
                'timestamp': event.timestamp,
                'properties': json.dumps(event.properties, ensure_ascii=False),
                'user_properties': json.dumps(event.user_properties, ensure_ascii=False),
                'device_info': json.dumps(event.device_info, ensure_ascii=False),
                'location_info': json.dumps(event.location_info, ensure_ascii=False)
            }

            self.client.execute(
                "INSERT INTO events VALUES",
                [data]
            )

            logger.info("Event tracked", event_type=event.event_type,
                        user_id=event.user_id)

        except Exception as e:
            logger.error("Failed to track event", error=str(e),
                         event_type=event.event_type)

    async def update_user_stats(self, user_id: str, properties: Dict[str, Any]):
        """Обновление статистики пользователя"""
        try:
            data = {
                'user_id': user_id,
                'registration_date': properties.get('registration_date', datetime.now(timezone.utc)),
                'last_activity': datetime.now(timezone.utc),
                'total_lessons_completed': properties.get('total_lessons_completed', 0),
                'total_time_spent': properties.get('total_time_spent', 0),
                'subscription_type': properties.get('subscription_type', 'free'),
                'user_properties': json.dumps(properties, ensure_ascii=False),
                'updated_at': datetime.now(timezone.utc)
            }

            self.client.execute(
                "INSERT INTO users VALUES",
                [data]
            )

        except Exception as e:
            logger.error("Failed to update user stats",
                         error=str(e), user_id=user_id)

    async def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Получение аналитики по пользователю"""
        try:
            # Основная статистика пользователя
            user_stats = self.client.execute(
                """
                SELECT 
                    total_lessons_completed,
                    total_time_spent,
                    subscription_type,
                    registration_date,
                    last_activity
                FROM users 
                WHERE user_id = %(user_id)s
                ORDER BY updated_at DESC
                LIMIT 1
                """,
                {'user_id': user_id}
            )

            # Активность по дням
            daily_activity = self.client.execute(
                """
                SELECT 
                    toDate(timestamp) as date,
                    count() as events_count,
                    countIf(event_type = 'lesson_complete') as lessons_completed,
                    countIf(event_type = 'ai_chat_message') as ai_interactions
                FROM events 
                WHERE user_id = %(user_id)s 
                AND timestamp >= now() - INTERVAL 30 DAY
                GROUP BY date
                ORDER BY date
                """,
                {'user_id': user_id}
            )

            # Прогресс по урокам
            lessons_progress = self.client.execute(
                """
                SELECT 
                    lesson_id,
                    max(progress_percent) as max_progress,
                    max(is_completed) as is_completed,
                    min(started_at) as first_attempt,
                    max(completed_at) as completed_at,
                    count() as attempts
                FROM lessons_analytics 
                WHERE user_id = %(user_id)s
                GROUP BY lesson_id
                ORDER BY first_attempt
                """,
                {'user_id': user_id}
            )

            return {
                'user_stats': user_stats[0] if user_stats else None,
                'daily_activity': daily_activity,
                'lessons_progress': lessons_progress
            }

        except Exception as e:
            logger.error("Failed to get user analytics",
                         error=str(e), user_id=user_id)
            return {}

    async def get_platform_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Получение общей аналитики платформы"""
        try:
            # Общая статистика
            overview = self.client.execute(
                """
                SELECT 
                    uniq(user_id) as total_users,
                    count() as total_events,
                    countIf(event_type = 'user_registration') as new_registrations,
                    countIf(event_type = 'lesson_complete') as lessons_completed,
                    countIf(event_type = 'ai_chat_message') as ai_interactions
                FROM events 
                WHERE timestamp >= now() - INTERVAL %(days)s DAY
                """,
                {'days': days}
            )

            # Активность по дням
            daily_metrics = self.client.execute(
                """
                SELECT 
                    date,
                    sum(events_count) as total_events,
                    sum(unique_users) as daily_active_users,
                    sumIf(events_count, event_type = 'lesson_complete') as lessons_completed
                FROM daily_stats 
                WHERE date >= today() - %(days)s
                GROUP BY date
                ORDER BY date
                """,
                {'days': days}
            )

            # Топ уроков
            top_lessons = self.client.execute(
                """
                SELECT 
                    lesson_id,
                    count() as completions,
                    uniq(user_id) as unique_users,
                    avg(duration_seconds) as avg_duration
                FROM lessons_analytics 
                WHERE is_completed = 1
                AND started_at >= now() - INTERVAL %(days)s DAY
                GROUP BY lesson_id
                ORDER BY completions DESC
                LIMIT 10
                """,
                {'days': days}
            )

            # Воронка конверсии
            funnel = self.client.execute(
                """
                SELECT 
                    countIf(event_type = 'user_registration') as registrations,
                    countIf(event_type = 'lesson_start') as lesson_starts,
                    countIf(event_type = 'lesson_complete') as lesson_completions,
                    countIf(event_type = 'course_enrollment') as course_enrollments,
                    countIf(event_type = 'payment_completed') as payments
                FROM events 
                WHERE timestamp >= now() - INTERVAL %(days)s DAY
                """,
                {'days': days}
            )

            return {
                'overview': overview[0] if overview else {},
                'daily_metrics': daily_metrics,
                'top_lessons': top_lessons,
                'funnel': funnel[0] if funnel else {}
            }

        except Exception as e:
            logger.error("Failed to get platform analytics", error=str(e))
            return {}

    async def get_real_time_metrics(self) -> Dict[str, Any]:
        """Получение метрик в реальном времени"""
        try:
            # Активность за последний час
            last_hour = self.client.execute(
                """
                SELECT 
                    count() as events_count,
                    uniq(user_id) as active_users,
                    uniq(session_id) as active_sessions
                FROM events 
                WHERE timestamp >= now() - INTERVAL 1 HOUR
                """
            )

            # События по типам за последний час
            events_by_type = self.client.execute(
                """
                SELECT 
                    event_type,
                    count() as count
                FROM events 
                WHERE timestamp >= now() - INTERVAL 1 HOUR
                GROUP BY event_type
                ORDER BY count DESC
                """
            )

            # Активные сессии
            active_sessions = self.client.execute(
                """
                SELECT count() as count
                FROM sessions 
                WHERE start_time >= now() - INTERVAL 1 HOUR
                AND (end_time IS NULL OR end_time >= now() - INTERVAL 30 MINUTE)
                """
            )

            return {
                'last_hour': last_hour[0] if last_hour else {},
                'events_by_type': events_by_type,
                'active_sessions': active_sessions[0]['count'] if active_sessions else 0
            }

        except Exception as e:
            logger.error("Failed to get real-time metrics", error=str(e))
            return {}


# Глобальный экземпляр аналитики
analytics = ClickHouseAnalytics()


# Декораторы для автоматического трекинга
def track_event_decorator(event_type: EventType, extract_properties: callable = None):
    """Декоратор для автоматического трекинга событий"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            import uuid
            from datetime import datetime, timezone

            result = await func(*args, **kwargs)

            # Извлекаем свойства события
            properties = {}
            if extract_properties:
                properties = extract_properties(*args, **kwargs, result=result)

            # Создаем событие
            event = AnalyticsEvent(
                event_id=str(uuid.uuid4()),
                event_type=event_type,
                timestamp=datetime.now(timezone.utc),
                properties=properties
            )

            # Отправляем в аналитику
            await analytics.track_event(event)

            return result
        return wrapper
    return decorator
