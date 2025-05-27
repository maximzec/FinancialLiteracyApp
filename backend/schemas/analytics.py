from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
from analytics import EventType


class AnalyticsEventCreate(BaseModel):
    """Схема для создания события аналитики"""
    event_type: EventType
    session_id: Optional[str] = None
    properties: Dict[str, Any] = {}
    user_properties: Dict[str, Any] = {}
    device_info: Dict[str, Any] = {}
    location_info: Dict[str, Any] = {}


class UserStats(BaseModel):
    """Статистика пользователя"""
    total_lessons_completed: int
    total_time_spent: int  # в секундах
    subscription_type: str
    registration_date: datetime
    last_activity: datetime


class DailyActivity(BaseModel):
    """Ежедневная активность"""
    date: str
    events_count: int
    lessons_completed: int
    ai_interactions: int


class LessonProgress(BaseModel):
    """Прогресс по урокам"""
    lesson_id: str
    max_progress: int  # процент
    is_completed: bool
    first_attempt: datetime
    completed_at: Optional[datetime]
    attempts: int


class UserAnalyticsResponse(BaseModel):
    """Ответ с аналитикой пользователя"""
    user_stats: Optional[UserStats]
    daily_activity: List[DailyActivity]
    lessons_progress: List[LessonProgress]


class PlatformOverview(BaseModel):
    """Общий обзор платформы"""
    total_users: int
    total_events: int
    new_registrations: int
    lessons_completed: int
    ai_interactions: int


class DailyMetrics(BaseModel):
    """Ежедневные метрики"""
    date: str
    total_events: int
    daily_active_users: int
    lessons_completed: int


class TopLesson(BaseModel):
    """Топ урок"""
    lesson_id: str
    completions: int
    unique_users: int
    avg_duration: float


class ConversionFunnel(BaseModel):
    """Воронка конверсии"""
    registrations: int
    lesson_starts: int
    lesson_completions: int
    course_enrollments: int
    payments: int


class PlatformAnalyticsResponse(BaseModel):
    """Ответ с аналитикой платформы"""
    overview: PlatformOverview
    daily_metrics: List[DailyMetrics]
    top_lessons: List[TopLesson]
    funnel: ConversionFunnel


class RealTimeOverview(BaseModel):
    """Обзор в реальном времени"""
    events_count: int
    active_users: int
    active_sessions: int


class EventTypeCount(BaseModel):
    """Количество событий по типам"""
    event_type: str
    count: int


class RealTimeMetricsResponse(BaseModel):
    """Ответ с метриками в реальном времени"""
    last_hour: RealTimeOverview
    events_by_type: List[EventTypeCount]
    active_sessions: int


class AnalyticsConfig(BaseModel):
    """Конфигурация аналитики"""
    clickhouse_host: str = Field(default="localhost")
    clickhouse_port: int = Field(default=9000)
    clickhouse_database: str = Field(default="analytics")
    retention_days: int = Field(default=365)
    batch_size: int = Field(default=1000)
    flush_interval: int = Field(default=60)  # секунды


class SessionInfo(BaseModel):
    """Информация о сессии"""
    session_id: str
    user_id: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    duration_seconds: Optional[int]
    page_views: int
    events_count: int
    device_info: Dict[str, Any]
    location_info: Dict[str, Any]
    referrer: Optional[str]


class LessonAnalytics(BaseModel):
    """Аналитика урока"""
    lesson_id: str
    user_id: str
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[int]
    progress_percent: int
    quiz_score: Optional[float]
    attempts_count: int
    is_completed: bool


class AnalyticsReport(BaseModel):
    """Отчет по аналитике"""
    report_id: str
    report_type: str
    period_start: datetime
    period_end: datetime
    data: Dict[str, Any]
    generated_at: datetime
    generated_by: str


class ExportRequest(BaseModel):
    """Запрос на экспорт данных"""
    user_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    event_types: Optional[List[EventType]] = None
    format: str = Field(default="json", regex="^(json|csv|xlsx)$")
    include_personal_data: bool = Field(default=False)


class DataRetentionPolicy(BaseModel):
    """Политика хранения данных"""
    events_retention_days: int = Field(default=365)
    user_data_retention_days: int = Field(default=1095)  # 3 года
    sessions_retention_days: int = Field(default=90)
    anonymize_after_days: int = Field(default=730)  # 2 года
    auto_delete_inactive_users: bool = Field(default=True)
    inactive_user_threshold_days: int = Field(default=1095)


class PrivacySettings(BaseModel):
    """Настройки приватности"""
    collect_ip_address: bool = Field(default=False)
    collect_user_agent: bool = Field(default=True)
    collect_referrer: bool = Field(default=True)
    collect_location: bool = Field(default=False)
    anonymize_ip: bool = Field(default=True)
    respect_do_not_track: bool = Field(default=True)
