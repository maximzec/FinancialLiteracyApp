from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from models.user import User
from models.gamification import (
    UserCoins, CoinTransaction, Challenge, UserChallenge,
    MassEvent, EventParticipant
)
from schemas.gamification import (
    ChallengeCreate, ChallengeUpdate, ChallengeResponse, UserChallengeResponse,
    MassEventCreate, MassEventUpdate, MassEventResponse, EventParticipantResponse,
    CoinTransactionResponse, UserCoinsResponse, GamificationStats,
    LeaderboardEntry, ChallengeProgress
)
from routers.auth import get_current_user_dependency
from services.kafka_service import KafkaService

router = APIRouter(prefix="/gamification", tags=["Gamification"])


# Челленджи
@router.post("/challenges", response_model=ChallengeResponse)
async def create_challenge(
    challenge: ChallengeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Создание нового челленджа (только для администраторов)"""
    # В реальном приложении здесь была бы проверка прав администратора

    db_challenge = Challenge(
        title=challenge.title,
        description=challenge.description,
        challenge_type=challenge.challenge_type,
        target_value=challenge.target_value,
        reward_coins=challenge.reward_coins,
        duration_days=challenge.duration_days,
        difficulty_level=challenge.difficulty_level,
        category=challenge.category
    )

    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)

    return db_challenge


@router.get("/challenges", response_model=List[ChallengeResponse])
async def get_challenges(
    category: Optional[str] = None,
    difficulty_level: Optional[str] = None,
    is_active: bool = True,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Получение списка челленджей"""
    query = db.query(Challenge).filter(Challenge.is_active == is_active)

    if category:
        query = query.filter(Challenge.category == category)
    if difficulty_level:
        query = query.filter(Challenge.difficulty_level == difficulty_level)

    challenges = query.offset(skip).limit(limit).all()
    return challenges


@router.get("/challenges/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(
    challenge_id: int,
    db: Session = Depends(get_db)
):
    """Получение челленджа по ID"""
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Челлендж не найден"
        )
    return challenge


@router.post("/challenges/{challenge_id}/join")
async def join_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Присоединение к челленджу"""
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Челлендж не найден"
        )

    # Проверяем, не участвует ли уже пользователь
    existing = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.challenge_id == challenge_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы уже участвуете в этом челлендже"
        )

    user_challenge = UserChallenge(
        user_id=current_user.id,
        challenge_id=challenge_id,
        current_progress=0
    )

    db.add(user_challenge)
    db.commit()

    # Отправляем событие в Kafka
    kafka_service = KafkaService()
    await kafka_service.publish_gamification_event({
        "event_type": "challenge_joined",
        "user_id": current_user.id,
        "challenge_id": challenge_id,
        "timestamp": datetime.utcnow().isoformat()
    })

    return {"message": "Успешно присоединились к челленджу"}


@router.get("/my-challenges", response_model=List[UserChallengeResponse])
async def get_my_challenges(
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение челленджей пользователя"""
    query = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id)

    if status_filter == "completed":
        query = query.filter(UserChallenge.is_completed == True)
    elif status_filter == "active":
        query = query.filter(UserChallenge.is_completed == False)

    user_challenges = query.all()
    return user_challenges


@router.get("/challenges/{challenge_id}/progress", response_model=ChallengeProgress)
async def get_challenge_progress(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение прогресса по челленджу"""
    user_challenge = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.challenge_id == challenge_id
    ).first()

    if not user_challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вы не участвуете в этом челлендже"
        )

    challenge = user_challenge.challenge
    progress_percentage = (
        user_challenge.current_progress / challenge.target_value) * 100

    # Вычисляем оставшиеся дни
    days_passed = (datetime.utcnow() - user_challenge.started_at).days
    days_remaining = max(0, challenge.duration_days - days_passed)

    return ChallengeProgress(
        challenge_id=challenge_id,
        title=challenge.title,
        current_progress=user_challenge.current_progress,
        target_value=challenge.target_value,
        progress_percentage=progress_percentage,
        days_remaining=days_remaining,
        is_completed=user_challenge.is_completed
    )


# Массовые события
@router.post("/events", response_model=MassEventResponse)
async def create_mass_event(
    event: MassEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Создание массового события (только для администраторов)"""
    db_event = MassEvent(
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        start_date=event.start_date,
        end_date=event.end_date,
        target_participants=event.target_participants,
        reward_per_participant=event.reward_per_participant,
        requirements=event.requirements
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


@router.get("/events", response_model=List[MassEventResponse])
async def get_mass_events(
    is_active: bool = True,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получение списка массовых событий"""
    query = db.query(MassEvent).filter(MassEvent.is_active == is_active)

    if is_active:
        now = datetime.utcnow()
        query = query.filter(
            MassEvent.start_date <= now,
            MassEvent.end_date >= now
        )

    events = query.offset(skip).limit(limit).all()
    return events


@router.post("/events/{event_id}/join")
async def join_mass_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Присоединение к массовому событию"""
    event = db.query(MassEvent).filter(MassEvent.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие не найдено"
        )

    # Проверяем, не участвует ли уже пользователь
    existing = db.query(EventParticipant).filter(
        EventParticipant.user_id == current_user.id,
        EventParticipant.event_id == event_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы уже участвуете в этом событии"
        )

    participant = EventParticipant(
        user_id=current_user.id,
        event_id=event_id,
        participation_score=0
    )

    db.add(participant)

    # Обновляем счетчик участников
    event.current_participants += 1

    db.commit()

    return {"message": "Успешно присоединились к событию"}


# Коины и транзакции
@router.get("/coins", response_model=UserCoinsResponse)
async def get_user_coins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение баланса коинов пользователя"""
    user_coins = db.query(UserCoins).filter(
        UserCoins.user_id == current_user.id).first()

    if not user_coins:
        # Создаем запись если её нет
        user_coins = UserCoins(
            user_id=current_user.id,
            current_balance=0,
            total_earned=0,
            total_spent=0
        )
        db.add(user_coins)
        db.commit()
        db.refresh(user_coins)

    return user_coins


@router.get("/transactions", response_model=List[CoinTransactionResponse])
async def get_coin_transactions(
    transaction_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение истории транзакций коинов"""
    query = db.query(CoinTransaction).filter(
        CoinTransaction.user_id == current_user.id)

    if transaction_type:
        query = query.filter(
            CoinTransaction.transaction_type == transaction_type)

    transactions = query.order_by(
        CoinTransaction.created_at.desc()).offset(skip).limit(limit).all()
    return transactions


# Статистика и лидерборды
@router.get("/stats", response_model=GamificationStats)
async def get_gamification_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение статистики геймификации пользователя"""
    user_coins = db.query(UserCoins).filter(
        UserCoins.user_id == current_user.id).first()

    active_challenges = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.is_completed == False
    ).count()

    completed_challenges = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.is_completed == True
    ).count()

    active_events = db.query(EventParticipant).filter(
        EventParticipant.user_id == current_user.id
    ).count()

    return GamificationStats(
        total_coins=user_coins.current_balance if user_coins else 0,
        active_challenges=active_challenges,
        completed_challenges=completed_challenges,
        active_events=active_events,
        participated_events=active_events,
        current_streak=0,  # Можно добавить логику подсчета
        total_achievements=completed_challenges
    )


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Получение таблицы лидеров"""
    # Получаем топ пользователей по коинам
    top_users = db.query(UserCoins, User).join(User).order_by(
        UserCoins.current_balance.desc()
    ).limit(limit).all()

    leaderboard = []
    for rank, (user_coins, user) in enumerate(top_users, 1):
        completed_challenges = db.query(UserChallenge).filter(
            UserChallenge.user_id == user.id,
            UserChallenge.is_completed == True
        ).count()

        leaderboard.append(LeaderboardEntry(
            user_id=user.id,
            username=f"{user.first_name} {user.last_name}" if user.first_name else user.email,
            total_coins=user_coins.current_balance,
            completed_challenges=completed_challenges,
            rank=rank
        ))

    return leaderboard
