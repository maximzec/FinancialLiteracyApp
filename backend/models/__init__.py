from .user import User, UserProfile
from .lesson import Lesson, LessonProgress, Quiz, QuizAnswer
from .gamification import UserCoins, Challenge, UserChallenge, MassEvent, CoinTransaction, EventParticipant
from .ai import PersonalPlan, LessonContent, QuizValidation, AIInteraction
from .vector_data import (
    KnowledgeBase, LessonEmbedding, UserInteraction,
    SearchQuery, ContentRecommendation, FinancialConcept
)

__all__ = [
    # User models
    "User",
    "UserProfile",

    # Lesson models
    "Lesson",
    "LessonProgress",
    "Quiz",
    "QuizAnswer",

    # Gamification models
    "UserCoins",
    "CoinTransaction",
    "Challenge",
    "UserChallenge",
    "MassEvent",
    "EventParticipant",

    # AI models
    "PersonalPlan",
    "LessonContent",
    "QuizValidation",
    "AIInteraction",

    # Vector data models
    "KnowledgeBase",
    "LessonEmbedding",
    "UserInteraction",
    "SearchQuery",
    "ContentRecommendation",
    "FinancialConcept",
]
