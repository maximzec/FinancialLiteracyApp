from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class PersonalPlan(Base):
    __tablename__ = "personal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_data = Column(JSON, nullable=False)  # структурированный план обучения
    difficulty_level = Column(String, nullable=False)
    estimated_duration_weeks = Column(Integer, nullable=False)
    goals = Column(JSON, nullable=False)  # цели пользователя
    current_step = Column(Integer, default=0)
    total_steps = Column(Integer, nullable=False)
    # active, completed, paused, cancelled
    status = Column(String, default="active")
    ai_model_version = Column(String, nullable=False)
    # промпт, использованный для генерации
    generation_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="personal_plans")


class LessonContent(Base):
    __tablename__ = "lesson_content"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    # explanation, example, exercise, summary
    content_type = Column(String, nullable=False)
    ai_generated_content = Column(Text, nullable=False)
    # general, personalized, adaptive
    personalization_level = Column(String, default="general")
    # beginner, intermediate, advanced
    target_audience = Column(String, nullable=True)
    language = Column(String, default="ru")
    ai_model_version = Column(String, nullable=False)
    generation_prompt = Column(Text, nullable=True)
    quality_score = Column(Float, nullable=True)  # оценка качества контента
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    lesson = relationship("Lesson", back_populates="content_ai")


class QuizValidation(Base):
    __tablename__ = "quiz_validations"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    user_answer = Column(Text, nullable=False)
    # результат валидации от AI
    ai_validation_result = Column(JSON, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    confidence_score = Column(Float, nullable=True)  # уверенность AI в оценке
    feedback = Column(Text, nullable=True)  # обратная связь от AI
    ai_model_version = Column(String, nullable=False)
    validation_prompt = Column(Text, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AIInteraction(Base):
    __tablename__ = "ai_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # plan_generation, content_creation, quiz_validation, chat
    interaction_type = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_version = Column(String, nullable=False)
    tokens_used = Column(Integer, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    cost_usd = Column(Float, nullable=True)
    status = Column(String, default="completed")  # pending, completed, failed
    error_message = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)  # дополнительные данные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
