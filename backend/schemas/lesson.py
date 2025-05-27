from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class LessonCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200,
                       description="Название урока")
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание урока")
    content: str = Field(..., min_length=10, description="Контент урока")
    difficulty_level: str = Field(
        ..., description="Уровень сложности: beginner, intermediate, advanced")
    category: str = Field(..., description="Категория урока")
    duration_minutes: int = Field(
        15, ge=1, le=180, description="Продолжительность в минутах")
    order_index: int = Field(..., ge=0, description="Порядковый номер урока")
    prerequisites: Optional[List[int]] = Field(
        default_factory=list, description="ID уроков-предпосылок")
    learning_objectives: Optional[List[str]] = Field(
        default_factory=list, description="Цели обучения")
    keywords: Optional[str] = Field(
        None, description="Ключевые слова для поиска")


class LessonUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    content: Optional[str] = Field(None, min_length=10)
    difficulty_level: Optional[str] = None
    category: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, ge=1, le=180)
    order_index: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    prerequisites: Optional[List[int]] = None
    learning_objectives: Optional[List[str]] = None
    keywords: Optional[str] = None


class LessonResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    content: str
    difficulty_level: str
    category: str
    duration_minutes: int
    order_index: int
    is_active: bool
    prerequisites: Optional[List[int]] = None
    learning_objectives: Optional[List[str]] = None
    keywords: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LessonProgressCreate(BaseModel):
    lesson_id: int
    status: str = Field(
        "not_started", description="Статус: not_started, in_progress, completed")


class LessonProgressUpdate(BaseModel):
    status: Optional[str] = None
    progress_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    time_spent_minutes: Optional[int] = Field(None, ge=0)


class LessonProgressResponse(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    status: str
    progress_percentage: float
    time_spent_minutes: int
    completed_at: Optional[datetime] = None
    started_at: datetime
    lesson: Optional[LessonResponse] = None

    class Config:
        from_attributes = True


class QuizCreate(BaseModel):
    lesson_id: int
    question: str = Field(..., min_length=10, description="Текст вопроса")
    question_type: str = Field(
        "multiple_choice", description="Тип вопроса: multiple_choice, true_false, text")
    options: Optional[List[str]] = Field(
        None, description="Варианты ответов для multiple choice")
    correct_answer: str = Field(..., description="Правильный ответ")
    explanation: Optional[str] = Field(
        None, description="Объяснение правильного ответа")
    points: int = Field(
        1, ge=1, le=10, description="Количество баллов за правильный ответ")
    order_index: int = Field(..., ge=0, description="Порядковый номер вопроса")


class QuizUpdate(BaseModel):
    question: Optional[str] = Field(None, min_length=10)
    question_type: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    points: Optional[int] = Field(None, ge=1, le=10)
    order_index: Optional[int] = Field(None, ge=0)


class QuizResponse(BaseModel):
    id: int
    lesson_id: int
    question: str
    question_type: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: Optional[str] = None
    points: int
    order_index: int

    class Config:
        from_attributes = True


class QuizAnswerCreate(BaseModel):
    quiz_id: int
    user_answer: str = Field(..., description="Ответ пользователя")


class QuizAnswerResponse(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    user_answer: str
    is_correct: bool
    points_earned: int
    answered_at: datetime
    quiz: Optional[QuizResponse] = None

    class Config:
        from_attributes = True


class LessonWithProgress(LessonResponse):
    user_progress: Optional[LessonProgressResponse] = None
    quizzes: Optional[List[QuizResponse]] = None


class LessonStats(BaseModel):
    total_lessons: int
    completed_lessons: int
    in_progress_lessons: int
    total_time_spent: int
    average_progress: float
    completion_rate: float
