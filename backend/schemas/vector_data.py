from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class KnowledgeBaseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200,
                       description="Заголовок знания")
    content: str = Field(..., min_length=10, description="Содержание знания")
    content_type: str = Field(
        ..., description="Тип контента: article, definition, example, tip, warning")
    category: str = Field(..., description="Категория знания")
    difficulty_level: str = Field(
        ..., description="Уровень сложности: beginner, intermediate, advanced")
    tags: Optional[str] = Field(None, description="Теги через запятую")
    source: Optional[str] = Field(None, description="Источник информации")


class KnowledgeBaseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    content_type: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    tags: Optional[str] = None
    source: Optional[str] = None
    is_verified: Optional[bool] = None


class KnowledgeBaseResponse(BaseModel):
    id: int
    title: str
    content: str
    content_type: str
    category: str
    difficulty_level: str
    tags: Optional[str] = None
    source: Optional[str] = None
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Поисковый запрос")
    content_types: Optional[List[str]] = Field(
        None, description="Фильтр по типам контента")
    categories: Optional[List[str]] = Field(
        None, description="Фильтр по категориям")
    difficulty_levels: Optional[List[str]] = Field(
        None, description="Фильтр по уровням сложности")
    limit: int = Field(10, ge=1, le=50, description="Количество результатов")


class SearchResult(BaseModel):
    content_type: str
    content_id: int
    title: str
    content: str
    category: str
    difficulty_level: str
    similarity: float
    source: Optional[str] = None
    duration_minutes: Optional[int] = None
    tags: Optional[str] = None


class RecommendationResult(BaseModel):
    content_type: str
    content_id: int
    title: str
    content: str
    category: str
    recommendation_type: str
    score: float
    reason: str
    estimated_time_minutes: Optional[int] = None


class UserInteractionCreate(BaseModel):
    interaction_type: str = Field(
        ..., description="Тип взаимодействия: search, view, like, bookmark, share")
    content_type: str = Field(...,
                              description="Тип контента: lesson, knowledge_base, quiz")
    content_id: int = Field(..., description="ID контента")
    query: Optional[str] = Field(
        None, description="Поисковый запрос если применимо")
    duration_seconds: Optional[int] = Field(
        None, ge=0, description="Время взаимодействия")
    rating: Optional[float] = Field(
        None, ge=1.0, le=5.0, description="Оценка контента")


class UserInteractionResponse(BaseModel):
    id: int
    user_id: int
    interaction_type: str
    content_type: str
    content_id: int
    query: Optional[str] = None
    duration_seconds: Optional[int] = None
    rating: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SearchQueryResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    query: str
    results_count: int
    clicked_result_id: Optional[int] = None
    session_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ContentRecommendationResponse(BaseModel):
    id: int
    user_id: int
    content_type: str
    content_id: int
    recommendation_type: str
    score: float
    reason: Optional[str] = None
    is_shown: bool
    is_clicked: bool
    created_at: datetime

    class Config:
        from_attributes = True


class FinancialConceptCreate(BaseModel):
    term: str = Field(..., min_length=1, max_length=100,
                      description="Финансовый термин")
    definition: str = Field(..., min_length=10,
                            description="Определение термина")
    simple_explanation: Optional[str] = Field(
        None, description="Простое объяснение")
    examples: Optional[str] = Field(None, description="Примеры использования")
    related_terms: Optional[str] = Field(
        None, description="Связанные термины через запятую")
    category: str = Field(..., description="Категория концепции")
    difficulty_level: str = Field(..., description="Уровень сложности")


class FinancialConceptUpdate(BaseModel):
    term: Optional[str] = Field(None, min_length=1, max_length=100)
    definition: Optional[str] = Field(None, min_length=10)
    simple_explanation: Optional[str] = None
    examples: Optional[str] = None
    related_terms: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None


class FinancialConceptResponse(BaseModel):
    id: int
    term: str
    definition: str
    simple_explanation: Optional[str] = None
    examples: Optional[str] = None
    related_terms: Optional[str] = None
    category: str
    difficulty_level: str
    usage_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VectorSearchStats(BaseModel):
    total_searches: int
    unique_users: int
    popular_queries: List[Dict[str, Any]]
    top_categories: List[Dict[str, Any]]
    average_results_per_search: float


class SimilarityMatch(BaseModel):
    content_id: int
    content_type: str
    title: str
    similarity_score: float
    match_reason: str


class EmbeddingResponse(BaseModel):
    content_id: int
    content_type: str
    embedding_created: bool
    processing_time_ms: int
    message: str
