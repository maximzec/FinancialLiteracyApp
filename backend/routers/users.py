from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.user import User, UserProfile
from models.lesson import LessonProgress
from models.gamification import UserCoins, UserChallenge
from schemas.user import (
    UserResponse, UserProfileCreate, UserProfileUpdate, UserProfileResponse,
    UserWithProfile
)
from schemas.lesson import LessonStats
from routers.auth import get_current_user_dependency

router = APIRouter(prefix="/users", tags=["Users & Profiles"])


@router.get("/me", response_model=UserWithProfile)
async def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение профиля текущего пользователя"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id).first()

    user_data = UserWithProfile(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        profile=profile
    )

    return user_data


@router.post("/profile", response_model=UserProfileResponse)
async def create_user_profile(
    profile_data: UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Создание профиля пользователя"""
    # Проверяем, есть ли уже профиль
    existing_profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Профиль уже существует. Используйте PUT для обновления."
        )

    profile = UserProfile(
        user_id=current_user.id,
        age=profile_data.age,
        financial_experience=profile_data.financial_experience,
        monthly_income=profile_data.monthly_income,
        financial_goals=profile_data.financial_goals,
        risk_tolerance=profile_data.risk_tolerance,
        preferred_learning_style=profile_data.preferred_learning_style,
        goals=profile_data.goals
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Обновление профиля пользователя"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль не найден. Создайте профиль сначала."
        )

    # Обновляем только переданные поля
    update_data = profile_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение профиля пользователя"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль не найден"
        )

    return profile


@router.delete("/profile")
async def delete_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Удаление профиля пользователя"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль не найден"
        )

    db.delete(profile)
    db.commit()

    return {"message": "Профиль успешно удален"}


@router.get("/stats", response_model=LessonStats)
async def get_user_learning_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение статистики обучения пользователя"""
    # Получаем прогресс по урокам
    progress_records = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id
    ).all()

    total_lessons = len(progress_records)
    completed_lessons = len(
        [p for p in progress_records if p.status == "completed"])
    in_progress_lessons = len(
        [p for p in progress_records if p.status == "in_progress"])
    total_time_spent = sum(p.time_spent_minutes for p in progress_records)

    # Вычисляем средний прогресс
    if progress_records:
        average_progress = sum(
            p.progress_percentage for p in progress_records) / len(progress_records)
        completion_rate = (completed_lessons / total_lessons) * 100
    else:
        average_progress = 0.0
        completion_rate = 0.0

    return LessonStats(
        total_lessons=total_lessons,
        completed_lessons=completed_lessons,
        in_progress_lessons=in_progress_lessons,
        total_time_spent=total_time_spent,
        average_progress=average_progress,
        completion_rate=completion_rate
    )


@router.get("/dashboard")
async def get_user_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение данных для дашборда пользователя"""
    # Статистика обучения
    progress_records = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id
    ).all()

    completed_lessons = len(
        [p for p in progress_records if p.status == "completed"])
    in_progress_lessons = len(
        [p for p in progress_records if p.status == "in_progress"])

    # Статистика геймификации
    user_coins = db.query(UserCoins).filter(
        UserCoins.user_id == current_user.id).first()
    active_challenges = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.is_completed == False
    ).count()

    # Последние активности
    recent_progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id
    ).order_by(LessonProgress.started_at.desc()).limit(5).all()

    return {
        "learning_stats": {
            "completed_lessons": completed_lessons,
            "in_progress_lessons": in_progress_lessons,
            "total_time_spent": sum(p.time_spent_minutes for p in progress_records),
        },
        "gamification_stats": {
            "total_coins": user_coins.current_balance if user_coins else 0,
            "active_challenges": active_challenges,
        },
        "recent_activities": [
            {
                "lesson_id": p.lesson_id,
                "status": p.status,
                "progress": p.progress_percentage,
                "last_activity": p.started_at
            }
            for p in recent_progress
        ]
    }


@router.get("/achievements")
async def get_user_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение достижений пользователя"""
    # Получаем статистику для расчета достижений
    progress_records = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id
    ).all()

    completed_lessons = len(
        [p for p in progress_records if p.status == "completed"])
    total_time_spent = sum(p.time_spent_minutes for p in progress_records)

    completed_challenges = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.is_completed == True
    ).count()

    user_coins = db.query(UserCoins).filter(
        UserCoins.user_id == current_user.id).first()
    total_coins = user_coins.total_earned if user_coins else 0

    # Определяем достижения
    achievements = []

    # Достижения за уроки
    if completed_lessons >= 1:
        achievements.append({
            "id": "first_lesson",
            "title": "Первый шаг",
            "description": "Завершили первый урок",
            "icon": "🎯",
            "earned_at": "2024-01-01"  # В реальном приложении - дата получения
        })

    if completed_lessons >= 10:
        achievements.append({
            "id": "ten_lessons",
            "title": "Ученик",
            "description": "Завершили 10 уроков",
            "icon": "📚",
            "earned_at": "2024-01-15"
        })

    if completed_lessons >= 50:
        achievements.append({
            "id": "fifty_lessons",
            "title": "Эксперт",
            "description": "Завершили 50 уроков",
            "icon": "🏆",
            "earned_at": "2024-02-01"
        })

    # Достижения за время обучения
    if total_time_spent >= 60:  # 1 час
        achievements.append({
            "id": "one_hour",
            "title": "Час знаний",
            "description": "Потратили час на обучение",
            "icon": "⏰",
            "earned_at": "2024-01-05"
        })

    # Достижения за челленджи
    if completed_challenges >= 1:
        achievements.append({
            "id": "first_challenge",
            "title": "Принял вызов",
            "description": "Завершили первый челлендж",
            "icon": "💪",
            "earned_at": "2024-01-10"
        })

    # Достижения за коины
    if total_coins >= 100:
        achievements.append({
            "id": "hundred_coins",
            "title": "Коллекционер",
            "description": "Заработали 100 коинов",
            "icon": "💰",
            "earned_at": "2024-01-20"
        })

    return {
        "total_achievements": len(achievements),
        "achievements": achievements,
        "next_achievements": [
            {
                "id": "hundred_lessons",
                "title": "Мастер",
                "description": "Завершите 100 уроков",
                "icon": "🎓",
                "progress": completed_lessons,
                "target": 100
            },
            {
                "id": "thousand_coins",
                "title": "Богач",
                "description": "Заработайте 1000 коинов",
                "icon": "💎",
                "progress": total_coins,
                "target": 1000
            }
        ]
    }


@router.get("/preferences")
async def get_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение настроек пользователя"""
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id).first()

    return {
        "notifications": {
            "email_lessons": True,
            "email_challenges": True,
            "push_reminders": True,
            "weekly_reports": True
        },
        "learning": {
            "preferred_style": profile.preferred_learning_style if profile else "visual",
            "difficulty_level": profile.financial_experience if profile else "beginner",
            "daily_goal_minutes": 30,
            "reminder_time": "18:00"
        },
        "privacy": {
            "profile_visibility": "private",
            "show_in_leaderboard": True,
            "data_analytics": True
        }
    }


@router.put("/preferences")
async def update_user_preferences(
    preferences: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Обновление настроек пользователя"""
    # В реальном приложении здесь была бы отдельная таблица для настроек
    # Пока просто возвращаем подтверждение

    return {
        "message": "Настройки успешно обновлены",
        "updated_preferences": preferences
    }


@router.delete("/account")
async def delete_user_account(
    confirmation: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Удаление аккаунта пользователя"""
    if confirmation != "DELETE_MY_ACCOUNT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверное подтверждение удаления"
        )

    # В реальном приложении здесь была бы логика:
    # 1. Удаление всех связанных данных
    # 2. Анонимизация данных для аналитики
    # 3. Отправка уведомления

    # Пока просто деактивируем пользователя
    current_user.is_active = False
    db.commit()

    return {"message": "Аккаунт успешно деактивирован"}
