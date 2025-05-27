from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class UserCoins(Base):
    __tablename__ = "user_coins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),
                     unique=True, nullable=False)
    total_coins = Column(Integer, default=0)
    spent_coins = Column(Integer, default=0)
    available_coins = Column(Integer, default=0)
    last_daily_bonus = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="coins")
    transactions = relationship("CoinTransaction", back_populates="user_coins")


class CoinTransaction(Base):
    __tablename__ = "coin_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_coins_id = Column(Integer, ForeignKey(
        "user_coins.id"), nullable=False)
    # положительное для начисления, отрицательное для трат
    amount = Column(Integer, nullable=False)
    # lesson_completion, challenge_completion, daily_bonus, purchase
    transaction_type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # дополнительная информация о транзакции
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_coins = relationship("UserCoins", back_populates="transactions")


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    # daily, weekly, monthly, special
    challenge_type = Column(String, nullable=False)
    requirements = Column(JSON, nullable=False)  # условия выполнения
    reward_coins = Column(Integer, nullable=False)
    reward_items = Column(JSON, nullable=True)  # дополнительные награды
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    max_participants = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_challenges = relationship("UserChallenge", back_populates="challenge")


class UserChallenge(Base):
    __tablename__ = "user_challenges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    # active, completed, failed, expired
    status = Column(String, default="active")
    progress = Column(JSON, default={})  # прогресс выполнения
    completed_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="challenges")
    challenge = relationship("Challenge", back_populates="user_challenges")


class MassEvent(Base):
    __tablename__ = "mass_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    # competition, marathon, festival
    event_type = Column(String, nullable=False)
    rules = Column(JSON, nullable=False)
    rewards = Column(JSON, nullable=False)  # структура наград для разных мест
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    registration_deadline = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    max_participants = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    participants = relationship("EventParticipant", back_populates="event")


class EventParticipant(Base):
    __tablename__ = "event_participants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("mass_events.id"), nullable=False)
    score = Column(Integer, default=0)
    rank = Column(Integer, nullable=True)
    # registered, active, completed, disqualified
    status = Column(String, default="registered")
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    event = relationship("MassEvent", back_populates="participants")
