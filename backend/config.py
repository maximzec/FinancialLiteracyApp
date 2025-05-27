import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/financial_literacy"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_USER_EVENTS: str = "user-events"
    KAFKA_TOPIC_LESSON_EVENTS: str = "lesson-events"
    KAFKA_TOPIC_GAMIFICATION: str = "gamification-events"

    # Kubernetes
    KUBERNETES_NAMESPACE: str = "financial-literacy"

    # Gamification
    COINS_PER_LESSON: int = 10
    COINS_PER_CHALLENGE: int = 50
    DAILY_LOGIN_BONUS: int = 5

    # Application
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Financial Literacy App"

    class Config:
        env_file = ".env"


settings = Settings()
