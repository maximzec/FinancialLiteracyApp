from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PersonalPlanCreate(BaseModel):
    goals: List[str] = Field(..., min_items=1,
                             description="Финансовые цели пользователя")
    experience_level: str = Field(
        ..., description="Уровень опыта: beginner, intermediate, advanced")
    preferences: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Предпочтения обучения")
    time_commitment_hours: Optional[int] = Field(
        None, ge=1, le=40, description="Часов в неделю на обучение")


class PersonalPlanResponse(BaseModel):
    id: int
    user_id: int
    plan_data: Dict[str, Any]
    difficulty_level: str
    estimated_duration_weeks: int
    goals: List[str]
    total_steps: int
    current_step: int
    completion_percentage: float
    ai_model_version: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LessonContentRequest(BaseModel):
    lesson_id: int
    content_type: str = Field(
        "explanation", description="Тип контента: explanation, summary, examples, exercises")
    personalization_level: str = Field(
        "adaptive", description="Уровень персонализации")


class LessonContentResponse(BaseModel):
    id: int
    lesson_id: int
    content_type: str
    ai_generated_content: str
    personalization_level: str
    target_audience: str
    ai_model_version: str
    quality_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class QuizValidationRequest(BaseModel):
    quiz_id: int
    user_answer: str = Field(..., description="Ответ пользователя")


class QuizValidationResponse(BaseModel):
    id: int
    quiz_id: int
    user_answer: str
    ai_validation_result: Dict[str, Any]
    is_correct: bool
    confidence_score: float
    feedback: str
    ai_model_version: str
    processing_time_ms: int
    created_at: datetime

    class Config:
        from_attributes = True


class AIInteractionResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    interaction_type: str
    prompt: str
    response: str
    model_version: str
    tokens_used: Optional[int] = None
    processing_time_ms: Optional[int] = None
    status: str
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConceptGenerationRequest(BaseModel):
    category: str = Field(..., description="Категория финансовых концепций")
    difficulty_level: str = Field(..., description="Уровень сложности")
    count: int = Field(
        10, ge=1, le=50, description="Количество концепций для генерации")


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

    class Config:
        from_attributes = True


class AIContentAnalysis(BaseModel):
    content_quality: float
    readability_score: float
    educational_value: float
    engagement_level: float
    recommendations: List[str]


class PersonalizedRecommendation(BaseModel):
    content_type: str
    content_id: int
    title: str
    reason: str
    confidence: float
    estimated_time_minutes: int


class LearningPathStep(BaseModel):
    step_number: int
    title: str
    description: str
    estimated_duration_hours: int
    prerequisites: List[str]
    learning_objectives: List[str]
    resources: List[str]
    assessment_criteria: List[str]


class AITutorResponse(BaseModel):
    response_text: str
    confidence: float
    suggested_actions: List[str]
    related_concepts: List[str]
    follow_up_questions: List[str]
    difficulty_adjustment: Optional[str] = None
