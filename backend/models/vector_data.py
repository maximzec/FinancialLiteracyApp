from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from database import Base


class KnowledgeBase(Base):
    """База знаний по финансовой грамотности"""
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    # article, definition, example, tip, warning
    content_type = Column(String, nullable=False)
    # budgeting, investing, saving, credit, etc.
    category = Column(String, nullable=False, index=True)
    # beginner, intermediate, advanced
    difficulty_level = Column(String, nullable=False)
    tags = Column(String, nullable=True)  # comma-separated tags
    source = Column(String, nullable=True)  # источник информации
    embedding = Column(Vector(1536), nullable=True)  # OpenAI embedding vector
    is_verified = Column(Boolean, default=False)  # проверено экспертами
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class LessonEmbedding(Base):
    """Векторные представления уроков для поиска и рекомендаций"""
    __tablename__ = "lesson_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    content_chunk = Column(Text, nullable=False)  # часть контента урока
    chunk_index = Column(Integer, nullable=False)  # порядковый номер части
    embedding = Column(Vector(1536), nullable=False)  # OpenAI embedding vector
    # дополнительные метаданные в JSON
    metadata = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    lesson = relationship("Lesson", back_populates="embeddings")


class UserInteraction(Base):
    """Взаимодействия пользователя для персонализации"""
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # search, view, like, bookmark, share
    interaction_type = Column(String, nullable=False)
    # lesson, knowledge_base, quiz
    content_type = Column(String, nullable=False)
    content_id = Column(Integer, nullable=False)
    query = Column(Text, nullable=True)  # поисковый запрос если применимо
    duration_seconds = Column(Integer, nullable=True)  # время взаимодействия
    rating = Column(Float, nullable=True)  # оценка контента пользователем
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SearchQuery(Base):
    """История поисковых запросов для аналитики"""
    __tablename__ = "search_queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    query = Column(Text, nullable=False)
    query_embedding = Column(Vector(1536), nullable=True)
    results_count = Column(Integer, default=0)
    clicked_result_id = Column(Integer, nullable=True)
    session_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ContentRecommendation(Base):
    """Рекомендации контента для пользователей"""
    __tablename__ = "content_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_type = Column(String, nullable=False)  # lesson, knowledge_base
    content_id = Column(Integer, nullable=False)
    # similar, next_step, trending, personalized
    recommendation_type = Column(String, nullable=False)
    score = Column(Float, nullable=False)  # оценка релевантности
    reason = Column(Text, nullable=True)  # объяснение рекомендации
    is_shown = Column(Boolean, default=False)
    is_clicked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FinancialConcept(Base):
    """Финансовые концепции и термины"""
    __tablename__ = "financial_concepts"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, nullable=False, unique=True, index=True)
    definition = Column(Text, nullable=False)
    simple_explanation = Column(Text, nullable=True)  # простое объяснение
    examples = Column(Text, nullable=True)  # примеры использования
    related_terms = Column(String, nullable=True)  # связанные термины
    category = Column(String, nullable=False)
    difficulty_level = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=True)
    usage_count = Column(Integer, default=0)  # сколько раз использовался
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
