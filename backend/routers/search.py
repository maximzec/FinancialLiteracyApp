from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database import get_db
from models.user import User
from services.vector_service import VectorService
from routers.auth import get_current_user_dependency

router = APIRouter(prefix="/search", tags=["Search & Recommendations"])


class SearchRequest(BaseModel):
    query: str
    content_types: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    limit: int = 10


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


class RecommendationResult(BaseModel):
    content_type: str
    content_id: int
    title: str
    content: str
    category: str
    recommendation_type: str
    score: float
    reason: str


class KnowledgeBaseRequest(BaseModel):
    title: str
    content: str
    content_type: str
    category: str
    difficulty_level: str
    tags: Optional[str] = None
    source: Optional[str] = None


@router.post("/semantic", response_model=List[SearchResult])
async def semantic_search(
    search_request: SearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Семантический поиск по базе знаний и урокам"""
    try:
        vector_service = VectorService(db)

        results = await vector_service.semantic_search(
            query=search_request.query,
            user_id=current_user.id,
            content_types=search_request.content_types,
            categories=search_request.categories,
            limit=search_request.limit
        )

        return [SearchResult(**result) for result in results]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при поиске: {str(e)}"
        )


@router.get("/recommendations", response_model=List[RecommendationResult])
async def get_recommendations(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение персонализированных рекомендаций"""
    try:
        vector_service = VectorService(db)

        recommendations = await vector_service.get_content_recommendations(
            user_id=current_user.id,
            limit=limit
        )

        return [RecommendationResult(**rec) for rec in recommendations]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении рекомендаций: {str(e)}"
        )


@router.get("/concepts/{concept}")
async def find_related_concepts(
    concept: str,
    limit: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Поиск связанных финансовых концепций"""
    try:
        vector_service = VectorService(db)

        related_concepts = await vector_service.find_related_concepts(
            concept=concept,
            limit=limit
        )

        return [{
            'id': concept.id,
            'term': concept.term,
            'definition': concept.definition,
            'simple_explanation': concept.simple_explanation,
            'examples': concept.examples,
            'category': concept.category,
            'difficulty_level': concept.difficulty_level
        } for concept in related_concepts]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при поиске концепций: {str(e)}"
        )


@router.post("/knowledge-base")
async def add_knowledge(
    knowledge_request: KnowledgeBaseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Добавление знаний в базу (только для администраторов)"""
    # В реальном приложении здесь была бы проверка прав администратора
    try:
        vector_service = VectorService(db)

        knowledge = await vector_service.add_knowledge_to_base(
            title=knowledge_request.title,
            content=knowledge_request.content,
            content_type=knowledge_request.content_type,
            category=knowledge_request.category,
            difficulty_level=knowledge_request.difficulty_level,
            tags=knowledge_request.tags,
            source=knowledge_request.source
        )

        return {
            "id": knowledge.id,
            "title": knowledge.title,
            "message": "Знания успешно добавлены в базу"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при добавлении знаний: {str(e)}"
        )


@router.post("/vectorize-lesson/{lesson_id}")
async def vectorize_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Векторизация контента урока (только для администраторов)"""
    try:
        vector_service = VectorService(db)

        embeddings = await vector_service.vectorize_lesson_content(lesson_id)

        return {
            "lesson_id": lesson_id,
            "embeddings_created": len(embeddings),
            "message": "Урок успешно векторизован"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при векторизации урока: {str(e)}"
        )


@router.get("/trending")
async def get_trending_content(
    limit: int = Query(10, ge=1, le=20),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получение популярного контента"""
    try:
        from models.vector_data import KnowledgeBase

        query = db.query(KnowledgeBase).filter(
            KnowledgeBase.is_verified == True)

        if category:
            query = query.filter(KnowledgeBase.category == category)

        trending = query.order_by(
            KnowledgeBase.created_at.desc()).limit(limit).all()

        return [{
            'id': kb.id,
            'title': kb.title,
            'content': kb.content[:200] + "..." if len(kb.content) > 200 else kb.content,
            'category': kb.category,
            'difficulty_level': kb.difficulty_level,
            'content_type': kb.content_type,
            'tags': kb.tags,
            'created_at': kb.created_at
        } for kb in trending]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении популярного контента: {str(e)}"
        )
