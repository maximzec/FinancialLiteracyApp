from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChallengeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200,
                       description="Название челленджа")
    description: str = Field(..., min_length=10,
                             description="Описание челленджа")
    challenge_type: str = Field(..., description="Тип челленджа")
    target_value: int = Field(..., ge=1, description="Целевое значение")
    reward_coins: int = Field(..., ge=1, description="Награда в коинах")
    duration_days: int = Field(..., ge=1, le=365,
                               description="Продолжительность в днях")
    difficulty_level: str = Field(..., description="Уровень сложности")
    category: str = Field(..., description="Категория челленджа")


class ChallengeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    challenge_type: Optional[str] = None
    target_value: Optional[int] = Field(None, ge=1)
    reward_coins: Optional[int] = Field(None, ge=1)
    duration_days: Optional[int] = Field(None, ge=1, le=365)
    difficulty_level: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class ChallengeResponse(BaseModel):
    id: int
    title: str
    description: str
    challenge_type: str
    target_value: int
    reward_coins: int
    duration_days: int
    difficulty_level: str
    category: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserChallengeResponse(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    current_progress: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    started_at: datetime
    challenge: Optional[ChallengeResponse] = None

    class Config:
        from_attributes = True


class MassEventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200,
                       description="Название события")
    description: str = Field(..., min_length=10,
                             description="Описание события")
    event_type: str = Field(..., description="Тип события")
    start_date: datetime = Field(..., description="Дата начала")
    end_date: datetime = Field(..., description="Дата окончания")
    target_participants: int = Field(..., ge=1,
                                     description="Целевое количество участников")
    reward_per_participant: int = Field(...,
                                        ge=1, description="Награда за участника")
    requirements: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Требования для участия")


class MassEventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    event_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    target_participants: Optional[int] = Field(None, ge=1)
    reward_per_participant: Optional[int] = Field(None, ge=1)
    requirements: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class MassEventResponse(BaseModel):
    id: int
    title: str
    description: str
    event_type: str
    start_date: datetime
    end_date: datetime
    target_participants: int
    current_participants: int
    reward_per_participant: int
    requirements: Optional[Dict[str, Any]] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EventParticipantResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    participation_score: int
    is_winner: bool
    reward_earned: int
    joined_at: datetime
    event: Optional[MassEventResponse] = None

    class Config:
        from_attributes = True


class CoinTransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: int
    transaction_type: str
    description: str
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserCoinsResponse(BaseModel):
    id: int
    user_id: int
    current_balance: int
    total_earned: int
    total_spent: int
    last_updated: datetime

    class Config:
        from_attributes = True


class GamificationStats(BaseModel):
    total_coins: int
    active_challenges: int
    completed_challenges: int
    active_events: int
    participated_events: int
    current_streak: int
    total_achievements: int


class LeaderboardEntry(BaseModel):
    user_id: int
    username: str
    total_coins: int
    completed_challenges: int
    rank: int


class ChallengeProgress(BaseModel):
    challenge_id: int
    title: str
    current_progress: int
    target_value: int
    progress_percentage: float
    days_remaining: int
    is_completed: bool
