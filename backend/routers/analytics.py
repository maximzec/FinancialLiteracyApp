from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import uuid

from analytics import analytics, AnalyticsEvent, EventType
from schemas.analytics import (
    AnalyticsEventCreate,
    UserAnalyticsResponse,
    PlatformAnalyticsResponse,
    RealTimeMetricsResponse
)
from dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/track")
async def track_event(
    event_data: AnalyticsEventCreate,
    current_user=Depends(get_current_user)
):
    """Отправка события в аналитику"""
    try:
        event = AnalyticsEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_data.event_type,
            user_id=current_user.id if current_user else None,
            session_id=event_data.session_id,
            timestamp=datetime.utcnow(),
            properties=event_data.properties,
            user_properties=event_data.user_properties,
            device_info=event_data.device_info,
            location_info=event_data.location_info
        )

        await analytics.track_event(event)

        return {"status": "success", "event_id": event.event_id}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to track event: {str(e)}")


@router.get("/user/{user_id}", response_model=UserAnalyticsResponse)
async def get_user_analytics(
    user_id: str,
    current_user=Depends(get_current_user)
):
    """Получение аналитики по пользователю"""
    try:
        # Проверяем права доступа (пользователь может смотреть только свою аналитику)
        if current_user.id != user_id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Access denied")

        data = await analytics.get_user_analytics(user_id)

        return UserAnalyticsResponse(**data)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get user analytics: {str(e)}")


@router.get("/platform", response_model=PlatformAnalyticsResponse)
async def get_platform_analytics(
    days: int = Query(30, ge=1, le=365,
                      description="Количество дней для анализа"),
    current_user=Depends(get_current_user)
):
    """Получение общей аналитики платформы (только для админов)"""
    try:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=403, detail="Admin access required")

        data = await analytics.get_platform_analytics(days)

        return PlatformAnalyticsResponse(**data)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get platform analytics: {str(e)}")


@router.get("/real-time", response_model=RealTimeMetricsResponse)
async def get_real_time_metrics(
    current_user=Depends(get_current_user)
):
    """Получение метрик в реальном времени (только для админов)"""
    try:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=403, detail="Admin access required")

        data = await analytics.get_real_time_metrics()

        return RealTimeMetricsResponse(**data)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get real-time metrics: {str(e)}")


@router.post("/lesson/start")
async def track_lesson_start(
    lesson_id: str,
    session_id: Optional[str] = None,
    current_user=Depends(get_current_user)
):
    """Отслеживание начала урока"""
    try:
        event = AnalyticsEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.LESSON_START,
            user_id=current_user.id,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            properties={"lesson_id": lesson_id}
        )

        await analytics.track_event(event)

        return {"status": "success"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to track lesson start: {str(e)}")


@router.post("/lesson/complete")
async def track_lesson_complete(
    lesson_id: str,
    duration_seconds: int,
    quiz_score: Optional[float] = None,
    session_id: Optional[str] = None,
    current_user=Depends(get_current_user)
):
    """Отслеживание завершения урока"""
    try:
        # Трекаем событие завершения урока
        event = AnalyticsEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.LESSON_COMPLETE,
            user_id=current_user.id,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            properties={
                "lesson_id": lesson_id,
                "duration_seconds": duration_seconds,
                "quiz_score": quiz_score
            }
        )

        await analytics.track_event(event)

        # Обновляем статистику пользователя
        await analytics.update_user_stats(
            current_user.id,
            {
                "total_lessons_completed": 1,  # Будет суммироваться
                "total_time_spent": duration_seconds
            }
        )

        return {"status": "success"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to track lesson completion: {str(e)}")


@router.post("/ai/chat")
async def track_ai_chat(
    message_type: str,
    response_time_ms: Optional[int] = None,
    session_id: Optional[str] = None,
    current_user=Depends(get_current_user)
):
    """Отслеживание AI чата"""
    try:
        event = AnalyticsEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.AI_CHAT_MESSAGE,
            user_id=current_user.id,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            properties={
                "message_type": message_type,
                "response_time_ms": response_time_ms
            }
        )

        await analytics.track_event(event)

        return {"status": "success"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to track AI chat: {str(e)}")


@router.get("/dashboard/overview")
async def get_dashboard_overview(
    current_user=Depends(get_current_user)
):
    """Получение данных для дашборда (краткий обзор)"""
    try:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=403, detail="Admin access required")

        # Получаем данные за последние 7 дней
        platform_data = await analytics.get_platform_analytics(7)
        real_time_data = await analytics.get_real_time_metrics()

        # Формируем краткий обзор
        overview = {
            "total_users_7d": platform_data.get("overview", {}).get("total_users", 0),
            "new_registrations_7d": platform_data.get("overview", {}).get("new_registrations", 0),
            "lessons_completed_7d": platform_data.get("overview", {}).get("lessons_completed", 0),
            "ai_interactions_7d": platform_data.get("overview", {}).get("ai_interactions", 0),
            "active_users_now": real_time_data.get("last_hour", {}).get("active_users", 0),
            "active_sessions_now": real_time_data.get("active_sessions", 0),
            "top_lessons": platform_data.get("top_lessons", [])[:5],
            "conversion_funnel": platform_data.get("funnel", {})
        }

        return overview

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get dashboard overview: {str(e)}")


@router.get("/export/user/{user_id}")
async def export_user_data(
    user_id: str,
    format: str = Query("json", regex="^(json|csv)$"),
    current_user=Depends(get_current_user)
):
    """Экспорт данных пользователя (GDPR compliance)"""
    try:
        # Проверяем права доступа
        if current_user.id != user_id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Access denied")

        data = await analytics.get_user_analytics(user_id)

        if format == "csv":
            # Конвертируем в CSV формат
            import csv
            import io

            output = io.StringIO()
            writer = csv.writer(output)

            # Записываем заголовки и данные
            writer.writerow(["Type", "Data"])
            for key, value in data.items():
                writer.writerow([key, str(value)])

            return {
                "format": "csv",
                "data": output.getvalue()
            }

        return {
            "format": "json",
            "data": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to export user data: {str(e)}")


@router.delete("/user/{user_id}")
async def delete_user_analytics(
    user_id: str,
    current_user=Depends(get_current_user)
):
    """Удаление аналитических данных пользователя (GDPR compliance)"""
    try:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=403, detail="Admin access required")

        # Удаляем данные пользователя из всех таблиц
        analytics.client.execute(
            "ALTER TABLE events DELETE WHERE user_id = %(user_id)s",
            {"user_id": user_id}
        )

        analytics.client.execute(
            "ALTER TABLE users DELETE WHERE user_id = %(user_id)s",
            {"user_id": user_id}
        )

        analytics.client.execute(
            "ALTER TABLE sessions DELETE WHERE user_id = %(user_id)s",
            {"user_id": user_id}
        )

        analytics.client.execute(
            "ALTER TABLE lessons_analytics DELETE WHERE user_id = %(user_id)s",
            {"user_id": user_id}
        )

        return {"status": "success", "message": "User analytics data deleted"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete user analytics: {str(e)}")
