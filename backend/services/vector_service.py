import openai
import tiktoken
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from models.vector_data import (
    KnowledgeBase, LessonEmbedding, UserInteraction,
    SearchQuery, ContentRecommendation, FinancialConcept
)
from models.lesson import Lesson
from models.user import User
from config import settings
import logging
import json
import re

logger = logging.getLogger(__name__)


class VectorService:
    def __init__(self, db: Session):
        self.db = db
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.encoding = tiktoken.encoding_for_model("text-embedding-ada-002")

    async def create_embedding(self, text: str) -> List[float]:
        """Создание векторного представления текста"""
        try:
            # Очищаем и подготавливаем текст
            cleaned_text = self._clean_text(text)

            # Проверяем длину токенов
            tokens = self.encoding.encode(cleaned_text)
            if len(tokens) > 8000:  # Лимит для embedding модели
                cleaned_text = self.encoding.decode(tokens[:8000])

            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=cleaned_text
            )

            return response.data[0].embedding

        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise

    async def add_knowledge_to_base(self, title: str, content: str, content_type: str,
                                    category: str, difficulty_level: str,
                                    tags: Optional[str] = None, source: Optional[str] = None) -> KnowledgeBase:
        """Добавление знаний в базу с векторизацией"""
        try:
            # Создаем embedding для контента
            embedding = await self.create_embedding(f"{title}\n{content}")

            knowledge = KnowledgeBase(
                title=title,
                content=content,
                content_type=content_type,
                category=category,
                difficulty_level=difficulty_level,
                tags=tags,
                source=source,
                embedding=embedding
            )

            self.db.add(knowledge)
            self.db.commit()
            self.db.refresh(knowledge)

            logger.info(f"Added knowledge to base: {title}")
            return knowledge

        except Exception as e:
            logger.error(f"Error adding knowledge to base: {e}")
            raise

    async def vectorize_lesson_content(self, lesson_id: int) -> List[LessonEmbedding]:
        """Векторизация контента урока по частям"""
        lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            raise ValueError(f"Lesson {lesson_id} not found")

        # Удаляем старые embeddings
        self.db.query(LessonEmbedding).filter(
            LessonEmbedding.lesson_id == lesson_id).delete()

        # Разбиваем контент на части
        chunks = self._split_content_into_chunks(
            lesson.content, max_tokens=500)

        embeddings = []
        for i, chunk in enumerate(chunks):
            try:
                # Создаем embedding для части
                embedding_vector = await self.create_embedding(chunk)

                lesson_embedding = LessonEmbedding(
                    lesson_id=lesson_id,
                    content_chunk=chunk,
                    chunk_index=i,
                    embedding=embedding_vector,
                    metadata=json.dumps({
                        "title": lesson.title,
                        "category": lesson.category,
                        "difficulty": lesson.difficulty_level
                    })
                )

                self.db.add(lesson_embedding)
                embeddings.append(lesson_embedding)

            except Exception as e:
                logger.error(
                    f"Error creating embedding for chunk {i} of lesson {lesson_id}: {e}")

        self.db.commit()
        logger.info(
            f"Created {len(embeddings)} embeddings for lesson {lesson_id}")
        return embeddings

    async def semantic_search(self, query: str, user_id: Optional[int] = None,
                              content_types: Optional[List[str]] = None,
                              categories: Optional[List[str]] = None,
                              limit: int = 10) -> List[Dict[str, Any]]:
        """Семантический поиск по базе знаний и урокам"""
        try:
            # Создаем embedding для запроса
            query_embedding = await self.create_embedding(query)

            # Сохраняем запрос в историю
            search_query = SearchQuery(
                user_id=user_id,
                query=query,
                query_embedding=query_embedding
            )
            self.db.add(search_query)

            results = []

            # Поиск в базе знаний
            kb_results = await self._search_knowledge_base(
                query_embedding, content_types, categories, limit//2
            )
            results.extend(kb_results)

            # Поиск в уроках
            lesson_results = await self._search_lessons(
                query_embedding, categories, limit//2
            )
            results.extend(lesson_results)

            # Сортируем по релевантности
            results.sort(key=lambda x: x['similarity'], reverse=True)
            results = results[:limit]

            # Обновляем количество результатов
            search_query.results_count = len(results)
            self.db.commit()

            # Логируем взаимодействие пользователя
            if user_id:
                await self._log_search_interaction(user_id, query, results)

            return results

        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            raise

    async def get_content_recommendations(self, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Получение персонализированных рекомендаций контента"""
        try:
            # Анализируем историю пользователя
            user_interactions = self.db.query(UserInteraction).filter(
                UserInteraction.user_id == user_id
            ).order_by(UserInteraction.created_at.desc()).limit(50).all()

            if not user_interactions:
                # Для новых пользователей возвращаем популярный контент
                return await self._get_trending_content(limit)

            # Создаем профиль интересов пользователя
            user_profile = await self._build_user_interest_profile(user_interactions)

            # Находим похожий контент
            recommendations = await self._find_similar_content(user_profile, user_id, limit)

            # Сохраняем рекомендации
            for rec in recommendations:
                content_rec = ContentRecommendation(
                    user_id=user_id,
                    content_type=rec['content_type'],
                    content_id=rec['content_id'],
                    recommendation_type=rec['recommendation_type'],
                    score=rec['score'],
                    reason=rec['reason']
                )
                self.db.add(content_rec)

            self.db.commit()
            return recommendations

        except Exception as e:
            logger.error(
                f"Error getting recommendations for user {user_id}: {e}")
            raise

    async def find_related_concepts(self, concept: str, limit: int = 5) -> List[FinancialConcept]:
        """Поиск связанных финансовых концепций"""
        try:
            concept_embedding = await self.create_embedding(concept)

            # Поиск похожих концепций по векторному сходству
            query = text("""
                SELECT *, (embedding <=> :query_embedding) as distance
                FROM financial_concepts
                WHERE embedding IS NOT NULL
                ORDER BY distance
                LIMIT :limit
            """)

            result = self.db.execute(query, {
                'query_embedding': concept_embedding,
                'limit': limit
            })

            concepts = []
            for row in result:
                concept_obj = self.db.query(FinancialConcept).filter(
                    FinancialConcept.id == row.id
                ).first()
                if concept_obj:
                    concepts.append(concept_obj)

            return concepts

        except Exception as e:
            logger.error(f"Error finding related concepts: {e}")
            raise

    async def _search_knowledge_base(self, query_embedding: List[float],
                                     content_types: Optional[List[str]],
                                     categories: Optional[List[str]],
                                     limit: int) -> List[Dict[str, Any]]:
        """Поиск в базе знаний"""
        query_parts = [
            "SELECT *, (embedding <=> :query_embedding) as distance FROM knowledge_base WHERE embedding IS NOT NULL"]
        params = {'query_embedding': query_embedding}

        if content_types:
            query_parts.append("AND content_type = ANY(:content_types)")
            params['content_types'] = content_types

        if categories:
            query_parts.append("AND category = ANY(:categories)")
            params['categories'] = categories

        query_parts.append("ORDER BY distance LIMIT :limit")
        params['limit'] = limit

        query = text(" ".join(query_parts))
        result = self.db.execute(query, params)

        results = []
        for row in result:
            results.append({
                'content_type': 'knowledge_base',
                'content_id': row.id,
                'title': row.title,
                'content': row.content[:200] + "..." if len(row.content) > 200 else row.content,
                'category': row.category,
                'difficulty_level': row.difficulty_level,
                'similarity': 1 - row.distance,
                'source': row.source
            })

        return results

    async def _search_lessons(self, query_embedding: List[float],
                              categories: Optional[List[str]],
                              limit: int) -> List[Dict[str, Any]]:
        """Поиск в уроках"""
        query_parts = ["""
            SELECT l.*, le.content_chunk, (le.embedding <=> :query_embedding) as distance
            FROM lessons l
            JOIN lesson_embeddings le ON l.id = le.lesson_id
            WHERE le.embedding IS NOT NULL
        """]
        params = {'query_embedding': query_embedding}

        if categories:
            query_parts.append("AND l.category = ANY(:categories)")
            params['categories'] = categories

        query_parts.append("ORDER BY distance LIMIT :limit")
        params['limit'] = limit

        query = text(" ".join(query_parts))
        result = self.db.execute(query, params)

        results = []
        seen_lessons = set()

        for row in result:
            if row.id not in seen_lessons:
                results.append({
                    'content_type': 'lesson',
                    'content_id': row.id,
                    'title': row.title,
                    'content': row.content_chunk,
                    'category': row.category,
                    'difficulty_level': row.difficulty_level,
                    'similarity': 1 - row.distance,
                    'duration_minutes': row.duration_minutes
                })
                seen_lessons.add(row.id)

        return results

    def _clean_text(self, text: str) -> str:
        """Очистка текста для векторизации"""
        # Удаляем HTML теги
        text = re.sub(r'<[^>]+>', '', text)
        # Удаляем лишние пробелы
        text = re.sub(r'\s+', ' ', text)
        # Удаляем специальные символы
        text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)
        return text.strip()

    def _split_content_into_chunks(self, content: str, max_tokens: int = 500) -> List[str]:
        """Разбивка контента на части для векторизации"""
        sentences = re.split(r'[.!?]+', content)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Проверяем, поместится ли предложение в текущий chunk
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            tokens = self.encoding.encode(test_chunk)

            if len(tokens) <= max_tokens:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    async def _log_search_interaction(self, user_id: int, query: str, results: List[Dict[str, Any]]):
        """Логирование поискового взаимодействия"""
        interaction = UserInteraction(
            user_id=user_id,
            interaction_type="search",
            content_type="search_results",
            content_id=0,
            query=query
        )
        self.db.add(interaction)

    async def _get_trending_content(self, limit: int) -> List[Dict[str, Any]]:
        """Получение популярного контента"""
        # Простая реализация - возвращаем недавно добавленный контент
        knowledge = self.db.query(KnowledgeBase).filter(
            KnowledgeBase.is_verified == True
        ).order_by(KnowledgeBase.created_at.desc()).limit(limit).all()

        return [{
            'content_type': 'knowledge_base',
            'content_id': kb.id,
            'title': kb.title,
            'content': kb.content[:200] + "...",
            'category': kb.category,
            'recommendation_type': 'trending',
            'score': 0.8,
            'reason': 'Популярный контент'
        } for kb in knowledge]

    async def _build_user_interest_profile(self, interactions: List[UserInteraction]) -> Dict[str, float]:
        """Построение профиля интересов пользователя"""
        categories = {}
        content_types = {}

        for interaction in interactions:
            # Весим взаимодействия по типу
            weight = {
                'view': 1.0,
                'like': 2.0,
                'bookmark': 3.0,
                'share': 2.5
            }.get(interaction.interaction_type, 1.0)

            # Учитываем время взаимодействия
            if interaction.duration_seconds:
                weight *= min(interaction.duration_seconds /
                              60, 5.0)  # максимум 5x за время

            # Получаем категорию контента
            if interaction.content_type == 'lesson':
                lesson = self.db.query(Lesson).filter(
                    Lesson.id == interaction.content_id).first()
                if lesson:
                    categories[lesson.category] = categories.get(
                        lesson.category, 0) + weight

            content_types[interaction.content_type] = content_types.get(
                interaction.content_type, 0) + weight

        return {
            'categories': categories,
            'content_types': content_types
        }

    async def _find_similar_content(self, user_profile: Dict[str, Any],
                                    user_id: int, limit: int) -> List[Dict[str, Any]]:
        """Поиск похожего контента на основе профиля пользователя"""
        recommendations = []

        # Получаем топ категории пользователя
        top_categories = sorted(
            user_profile['categories'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        for category, score in top_categories:
            # Находим контент в этой категории
            knowledge = self.db.query(KnowledgeBase).filter(
                KnowledgeBase.category == category,
                KnowledgeBase.is_verified == True
            ).limit(limit//len(top_categories)).all()

            for kb in knowledge:
                recommendations.append({
                    'content_type': 'knowledge_base',
                    'content_id': kb.id,
                    'title': kb.title,
                    'content': kb.content[:200] + "...",
                    'category': kb.category,
                    'recommendation_type': 'personalized',
                    'score': score / sum(user_profile['categories'].values()),
                    'reason': f'Основано на вашем интересе к категории "{category}"'
                })

        return recommendations[:limit]
