from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    # beginner, intermediate, advanced
    difficulty_level = Column(String, nullable=False)
    # budgeting, investing, saving, etc.
    category = Column(String, nullable=False)
    duration_minutes = Column(Integer, default=15)
    order_index = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    prerequisites = Column(JSON, nullable=True)  # список ID уроков-предпосылок
    learning_objectives = Column(JSON, nullable=True)  # цели обучения
    keywords = Column(Text, nullable=True)  # ключевые слова для поиска
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    progress = relationship("LessonProgress", back_populates="lesson")
    quizzes = relationship("Quiz", back_populates="lesson")
    content_ai = relationship("LessonContent", back_populates="lesson")
    embeddings = relationship("LessonEmbedding", back_populates="lesson")


class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    # not_started, in_progress, completed
    status = Column(String, default="not_started")
    progress_percentage = Column(Float, default=0.0)
    time_spent_minutes = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    question = Column(Text, nullable=False)
    # multiple_choice, true_false, text
    question_type = Column(String, default="multiple_choice")
    options = Column(JSON, nullable=True)  # для multiple choice вопросов
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    points = Column(Integer, default=1)
    order_index = Column(Integer, nullable=False)

    # Relationships
    lesson = relationship("Lesson", back_populates="quizzes")
    answers = relationship("QuizAnswer", back_populates="quiz")


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    user_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    points_earned = Column(Integer, default=0)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    quiz = relationship("Quiz", back_populates="answers")
