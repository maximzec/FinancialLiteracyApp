from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import get_db
from models.user import User
from models.lesson import Lesson, LessonProgress, Quiz, QuizAnswer
from routers.auth import get_current_user_dependency
from services.kafka_service import KafkaService

router = APIRouter(prefix="/lessons", tags=["Lessons"])


class LessonResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty_level: str
    category: str
    duration_minutes: int
    order_index: int

    class Config:
        from_attributes = True


class LessonProgressResponse(BaseModel):
    id: int
    lesson_id: int
    status: str
    progress_percentage: float
    time_spent_minutes: int

    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    id: int
    question: str
    question_type: str
    options: dict
    points: int

    class Config:
        from_attributes = True


class QuizAnswerRequest(BaseModel):
    quiz_id: int
    user_answer: str


@router.get("/", response_model=List[LessonResponse])
async def get_lessons(
    category: str = None,
    difficulty: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение списка уроков"""
    query = db.query(Lesson).filter(Lesson.is_active == True)

    if category:
        query = query.filter(Lesson.category == category)
    if difficulty:
        query = query.filter(Lesson.difficulty_level == difficulty)

    lessons = query.order_by(Lesson.order_index).all()
    return lessons


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение конкретного урока"""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Урок не найден"
        )

    return lesson


@router.post("/{lesson_id}/start")
async def start_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Начало прохождения урока"""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Урок не найден"
        )

    # Проверяем, есть ли уже прогресс
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()

    if not progress:
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            status="in_progress"
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)

    # Отправляем событие в Kafka
    kafka_service = KafkaService()
    await kafka_service.publish_lesson_event(
        user_id=current_user.id,
        lesson_id=lesson_id,
        event_type="lesson_started",
        data={"lesson_title": lesson.title}
    )

    return {"message": "Урок начат", "progress_id": progress.id}


@router.get("/{lesson_id}/quizzes", response_model=List[QuizResponse])
async def get_lesson_quizzes(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение тестов урока"""
    quizzes = db.query(Quiz).filter(
        Quiz.lesson_id == lesson_id
    ).order_by(Quiz.order_index).all()

    return quizzes


@router.post("/quiz/answer")
async def answer_quiz(
    answer_data: QuizAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Ответ на тест"""
    quiz = db.query(Quiz).filter(Quiz.id == answer_data.quiz_id).first()

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тест не найден"
        )

    # Проверяем правильность ответа
    is_correct = answer_data.user_answer.lower() == quiz.correct_answer.lower()
    points_earned = quiz.points if is_correct else 0

    # Сохраняем ответ
    quiz_answer = QuizAnswer(
        user_id=current_user.id,
        quiz_id=answer_data.quiz_id,
        user_answer=answer_data.user_answer,
        is_correct=is_correct,
        points_earned=points_earned
    )

    db.add(quiz_answer)
    db.commit()

    # Отправляем событие в Kafka
    kafka_service = KafkaService()
    await kafka_service.publish_lesson_event(
        user_id=current_user.id,
        lesson_id=quiz.lesson_id,
        event_type="quiz_answered",
        data={
            "quiz_id": answer_data.quiz_id,
            "is_correct": is_correct,
            "points_earned": points_earned
        }
    )

    return {
        "is_correct": is_correct,
        "points_earned": points_earned,
        "explanation": quiz.explanation
    }


@router.get("/progress/my", response_model=List[LessonProgressResponse])
async def get_my_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение прогресса пользователя"""
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id
    ).all()

    return progress
