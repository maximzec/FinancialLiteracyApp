# Этот файл делает директорию schemas Python пакетом

from .user import UserCreate, UserResponse, UserProfileCreate, UserProfileResponse, UserLogin, Token
from .lesson import LessonCreate, LessonResponse, LessonProgressResponse, QuizCreate, QuizResponse, QuizAnswerCreate, QuizAnswerResponse
from .gamification import ChallengeCreate, ChallengeResponse, MassEventCreate, MassEventResponse, CoinTransactionResponse
from .ai import PersonalPlanCreate, PersonalPlanResponse, LessonContentResponse, QuizValidationResponse
from .vector_data import KnowledgeBaseCreate, KnowledgeBaseResponse, SearchRequest, SearchResult, RecommendationResult

__all__ = [
    # User schemas
    "UserCreate",
    "UserResponse",
    "UserProfileCreate",
    "UserProfileResponse",
    "UserLogin",
    "Token",

    # Lesson schemas
    "LessonCreate",
    "LessonResponse",
    "LessonProgressResponse",
    "QuizCreate",
    "QuizResponse",
    "QuizAnswerCreate",
    "QuizAnswerResponse",

    # Gamification schemas
    "ChallengeCreate",
    "ChallengeResponse",
    "MassEventCreate",
    "MassEventResponse",
    "CoinTransactionResponse",

    # AI schemas
    "PersonalPlanCreate",
    "PersonalPlanResponse",
    "LessonContentResponse",
    "QuizValidationResponse",

    # Vector data schemas
    "KnowledgeBaseCreate",
    "KnowledgeBaseResponse",
    "SearchRequest",
    "SearchResult",
    "RecommendationResult",
]
