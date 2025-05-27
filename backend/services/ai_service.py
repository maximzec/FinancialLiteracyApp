import openai
import json
import time
import tiktoken
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from models.ai import PersonalPlan, LessonContent, QuizValidation, AIInteraction
from models.user import User, UserProfile
from models.lesson import Lesson, Quiz
from models.vector_data import KnowledgeBase, FinancialConcept
from config import settings
import logging

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self, db: Session):
        self.db = db
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.encoding = tiktoken.encoding_for_model("gpt-4")

    async def generate_personal_plan(self, user_id: int, goals: List[str],
                                     experience_level: str, preferences: Optional[Dict] = None) -> PersonalPlan:
        """Генерация персонального плана обучения с учетом базы знаний"""
        user = self.db.query(User).filter(User.id == user_id).first()
        profile = self.db.query(UserProfile).filter(
            UserProfile.user_id == user_id).first()

        # Получаем релевантные знания из базы
        relevant_knowledge = await self._get_relevant_knowledge_for_plan(goals, experience_level)

        prompt = self._build_enhanced_personal_plan_prompt(
            user, profile, goals, experience_level, relevant_knowledge, preferences
        )

        start_time = time.time()

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system",
                        "content": self._get_financial_expert_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000,
                functions=[self._get_plan_generation_function()],
                function_call={"name": "generate_learning_plan"}
            )

            processing_time = int((time.time() - start_time) * 1000)

            # Парсим ответ функции
            function_call = response.choices[0].message.function_call
            plan_data = json.loads(function_call.arguments)

            # Сохраняем план в базу данных
            personal_plan = PersonalPlan(
                user_id=user_id,
                plan_data=plan_data,
                difficulty_level=experience_level,
                estimated_duration_weeks=plan_data.get("duration_weeks", 12),
                goals=goals,
                total_steps=len(plan_data.get("learning_path", [])),
                ai_model_version=self.model,
                generation_prompt=prompt
            )

            self.db.add(personal_plan)
            self.db.commit()
            self.db.refresh(personal_plan)

            # Логируем взаимодействие с AI
            await self._log_ai_interaction(
                user_id=user_id,
                interaction_type="plan_generation",
                prompt=prompt,
                response=function_call.arguments,
                tokens_used=response.usage.total_tokens,
                processing_time_ms=processing_time
            )

            return personal_plan

        except Exception as e:
            await self._log_ai_interaction(
                user_id=user_id,
                interaction_type="plan_generation",
                prompt=prompt,
                response="",
                status="failed",
                error_message=str(e)
            )
            raise

    async def generate_adaptive_lesson_content(self, lesson_id: int, user_id: int,
                                               content_type: str = "explanation") -> LessonContent:
        """Генерация адаптивного контента урока под конкретного пользователя"""
        lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        user = self.db.query(User).filter(User.id == user_id).first()
        profile = self.db.query(UserProfile).filter(
            UserProfile.user_id == user_id).first()

        # Получаем контекст из базы знаний
        context_knowledge = await self._get_lesson_context(lesson)

        # Анализируем прогресс пользователя
        user_progress = await self._analyze_user_progress(user_id)

        prompt = self._build_adaptive_content_prompt(
            lesson, user, profile, content_type, context_knowledge, user_progress
        )

        start_time = time.time()

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system",
                        "content": self._get_educational_content_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2000,
                functions=[self._get_content_generation_function()],
                function_call={"name": "generate_educational_content"}
            )

            processing_time = int((time.time() - start_time) * 1000)

            # Парсим ответ функции
            function_call = response.choices[0].message.function_call
            content_data = json.loads(function_call.arguments)

            # Сохраняем контент в базу данных
            lesson_content = LessonContent(
                lesson_id=lesson_id,
                content_type=content_type,
                ai_generated_content=content_data.get("content", ""),
                personalization_level="adaptive",
                target_audience=profile.financial_experience if profile else "general",
                ai_model_version=self.model,
                generation_prompt=prompt,
                quality_score=await self._evaluate_content_quality(content_data.get("content", ""))
            )

            self.db.add(lesson_content)
            self.db.commit()
            self.db.refresh(lesson_content)

            # Логируем взаимодействие с AI
            await self._log_ai_interaction(
                user_id=user_id,
                interaction_type="adaptive_content_creation",
                prompt=prompt,
                response=function_call.arguments,
                tokens_used=response.usage.total_tokens,
                processing_time_ms=processing_time,
                metadata={"lesson_id": lesson_id, "content_type": content_type}
            )

            return lesson_content

        except Exception as e:
            await self._log_ai_interaction(
                user_id=user_id,
                interaction_type="adaptive_content_creation",
                prompt=prompt,
                response="",
                status="failed",
                error_message=str(e),
                metadata={"lesson_id": lesson_id, "content_type": content_type}
            )
            raise

    async def intelligent_quiz_validation(self, quiz_id: int, user_answer: str,
                                          user_id: int) -> QuizValidation:
        """Интеллектуальная валидация ответа с детальной обратной связью"""
        quiz = self.db.query(Quiz).filter(Quiz.id == quiz_id).first()
        lesson = self.db.query(Lesson).filter(
            Lesson.id == quiz.lesson_id).first()

        # Получаем контекст из базы знаний
        context = await self._get_quiz_context(quiz, lesson)

        prompt = self._build_intelligent_validation_prompt(
            quiz, user_answer, context)

        start_time = time.time()

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_quiz_validator_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800,
                functions=[self._get_quiz_validation_function()],
                function_call={"name": "validate_quiz_answer"}
            )

            processing_time = int((time.time() - start_time) * 1000)

            # Парсим ответ функции
            function_call = response.choices[0].message.function_call
            validation_result = json.loads(function_call.arguments)

            # Сохраняем результат валидации
            quiz_validation = QuizValidation(
                quiz_id=quiz_id,
                user_answer=user_answer,
                ai_validation_result=validation_result,
                is_correct=validation_result.get("is_correct", False),
                confidence_score=validation_result.get("confidence", 0.0),
                feedback=validation_result.get("detailed_feedback", ""),
                ai_model_version=self.model,
                validation_prompt=prompt,
                processing_time_ms=processing_time
            )

            self.db.add(quiz_validation)
            self.db.commit()
            self.db.refresh(quiz_validation)

            # Логируем взаимодействие с AI
            await self._log_ai_interaction(
                user_id=user_id,
                interaction_type="intelligent_quiz_validation",
                prompt=prompt,
                response=function_call.arguments,
                tokens_used=response.usage.total_tokens,
                processing_time_ms=processing_time,
                metadata={"quiz_id": quiz_id}
            )

            return quiz_validation

        except Exception as e:
            await self._log_ai_interaction(
                user_id=user_id,
                interaction_type="intelligent_quiz_validation",
                prompt=prompt,
                response="",
                status="failed",
                error_message=str(e),
                metadata={"quiz_id": quiz_id}
            )
            raise

    async def generate_financial_concepts(self, category: str, difficulty_level: str,
                                          count: int = 10) -> List[FinancialConcept]:
        """Генерация финансовых концепций и терминов"""
        prompt = f"""
        Сгенерируй {count} важных финансовых концепций для категории "{category}" 
        уровня сложности "{difficulty_level}". Для каждой концепции предоставь:
        - Термин
        - Определение
        - Простое объяснение
        - Примеры использования
        - Связанные термины
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system",
                        "content": self._get_concept_generator_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000,
                functions=[self._get_concept_generation_function()],
                function_call={"name": "generate_financial_concepts"}
            )

            # Парсим ответ функции
            function_call = response.choices[0].message.function_call
            concepts_data = json.loads(function_call.arguments)

            concepts = []
            for concept_data in concepts_data.get("concepts", []):
                # Создаем embedding для концепции
                from services.vector_service import VectorService
                vector_service = VectorService(self.db)

                concept_text = f"{concept_data['term']} {concept_data['definition']} {concept_data['simple_explanation']}"
                embedding = await vector_service.create_embedding(concept_text)

                concept = FinancialConcept(
                    term=concept_data["term"],
                    definition=concept_data["definition"],
                    simple_explanation=concept_data.get("simple_explanation"),
                    examples=concept_data.get("examples"),
                    related_terms=", ".join(
                        concept_data.get("related_terms", [])),
                    category=category,
                    difficulty_level=difficulty_level,
                    embedding=embedding
                )

                self.db.add(concept)
                concepts.append(concept)

            self.db.commit()

            # Логируем взаимодействие с AI
            await self._log_ai_interaction(
                interaction_type="concept_generation",
                prompt=prompt,
                response=function_call.arguments,
                tokens_used=response.usage.total_tokens,
                metadata={"category": category,
                          "difficulty_level": difficulty_level, "count": count}
            )

            return concepts

        except Exception as e:
            logger.error(f"Error generating financial concepts: {e}")
            raise

    # Системные промпты
    def _get_financial_expert_system_prompt(self) -> str:
        return """
        Ты эксперт по финансовой грамотности с многолетним опытом обучения людей финансам.
        Твоя задача - создавать персонализированные планы обучения, которые:
        1. Учитывают текущий уровень знаний пользователя
        2. Соответствуют его целям и предпочтениям
        3. Структурированы и практически применимы
        4. Включают прогрессивное усложнение материала
        5. Содержат конкретные действия и измеримые результаты
        """

    def _get_educational_content_system_prompt(self) -> str:
        return """
        Ты опытный педагог и эксперт по финансовой грамотности.
        Создавай образовательный контент, который:
        1. Адаптирован под уровень знаний конкретного пользователя
        2. Использует понятные примеры и аналогии
        3. Структурирован и легко воспринимается
        4. Включает практические советы и действия
        5. Мотивирует к дальнейшему обучению
        """

    def _get_quiz_validator_system_prompt(self) -> str:
        return """
        Ты эксперт по оценке знаний в области финансовой грамотности.
        При валидации ответов:
        1. Учитывай частично правильные ответы
        2. Давай конструктивную обратную связь
        3. Объясняй правильные ответы
        4. Предлагай дополнительные ресурсы для изучения
        5. Поощряй дальнейшее обучение
        """

    def _get_concept_generator_system_prompt(self) -> str:
        return """
        Ты эксперт по финансовой терминологии и концепциям.
        Генерируй финансовые концепции, которые:
        1. Актуальны и важны для изучения
        2. Соответствуют указанному уровню сложности
        3. Имеют четкие и понятные определения
        4. Включают практические примеры
        5. Связаны с другими важными концепциями
        """

    # Функции для OpenAI Function Calling
    def _get_plan_generation_function(self) -> Dict:
        return {
            "name": "generate_learning_plan",
            "description": "Генерирует персональный план обучения финансовой грамотности",
            "parameters": {
                "type": "object",
                "properties": {
                    "duration_weeks": {"type": "integer", "description": "Продолжительность плана в неделях"},
                    "learning_path": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "week": {"type": "integer"},
                                "topic": {"type": "string"},
                                "objectives": {"type": "array", "items": {"type": "string"}},
                                "activities": {"type": "array", "items": {"type": "string"}},
                                "resources": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    },
                    "milestones": {"type": "array", "items": {"type": "string"}},
                    "success_metrics": {"type": "array", "items": {"type": "string"}},
                    "recommendations": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["duration_weeks", "learning_path", "milestones"]
            }
        }

    def _get_content_generation_function(self) -> Dict:
        return {
            "name": "generate_educational_content",
            "description": "Генерирует образовательный контент для урока",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Основной контент"},
                    "key_points": {"type": "array", "items": {"type": "string"}},
                    "examples": {"type": "array", "items": {"type": "string"}},
                    "practical_tips": {"type": "array", "items": {"type": "string"}},
                    "next_steps": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["content", "key_points"]
            }
        }

    def _get_quiz_validation_function(self) -> Dict:
        return {
            "name": "validate_quiz_answer",
            "description": "Валидирует ответ на тест и дает обратную связь",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_correct": {"type": "boolean"},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    "detailed_feedback": {"type": "string"},
                    "explanation": {"type": "string"},
                    "additional_resources": {"type": "array", "items": {"type": "string"}},
                    "improvement_suggestions": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["is_correct", "confidence", "detailed_feedback"]
            }
        }

    def _get_concept_generation_function(self) -> Dict:
        return {
            "name": "generate_financial_concepts",
            "description": "Генерирует финансовые концепции и термины",
            "parameters": {
                "type": "object",
                "properties": {
                    "concepts": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "term": {"type": "string"},
                                "definition": {"type": "string"},
                                "simple_explanation": {"type": "string"},
                                "examples": {"type": "string"},
                                "related_terms": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["term", "definition"]
                        }
                    }
                },
                "required": ["concepts"]
            }
        }

    # Вспомогательные методы
    async def _get_relevant_knowledge_for_plan(self, goals: List[str], experience_level: str) -> List[KnowledgeBase]:
        """Получение релевантных знаний для создания плана"""
        knowledge = self.db.query(KnowledgeBase).filter(
            KnowledgeBase.difficulty_level == experience_level,
            KnowledgeBase.is_verified == True
        ).limit(10).all()
        return knowledge

    async def _get_lesson_context(self, lesson: Lesson) -> List[KnowledgeBase]:
        """Получение контекста для урока из базы знаний"""
        context = self.db.query(KnowledgeBase).filter(
            KnowledgeBase.category == lesson.category,
            KnowledgeBase.is_verified == True
        ).limit(5).all()
        return context

    async def _analyze_user_progress(self, user_id: int) -> Dict:
        """Анализ прогресса пользователя"""
        from models.lesson import LessonProgress

        progress = self.db.query(LessonProgress).filter(
            LessonProgress.user_id == user_id
        ).all()

        return {
            "completed_lessons": len([p for p in progress if p.status == "completed"]),
            "in_progress_lessons": len([p for p in progress if p.status == "in_progress"]),
            "total_time_spent": sum(p.time_spent_minutes for p in progress),
            "average_progress": sum(p.progress_percentage for p in progress) / len(progress) if progress else 0
        }

    async def _get_quiz_context(self, quiz: Quiz, lesson: Lesson) -> str:
        """Получение контекста для валидации теста"""
        context_knowledge = self.db.query(KnowledgeBase).filter(
            KnowledgeBase.category == lesson.category
        ).limit(3).all()

        context = f"Урок: {lesson.title}\nКатегория: {lesson.category}\n"
        if context_knowledge:
            context += "Дополнительный контекст:\n"
            for kb in context_knowledge:
                context += f"- {kb.title}: {kb.content[:200]}...\n"

        return context

    def _build_enhanced_personal_plan_prompt(self, user: User, profile: UserProfile,
                                             goals: List[str], experience_level: str,
                                             relevant_knowledge: List[KnowledgeBase],
                                             preferences: Optional[Dict]) -> str:
        """Построение улучшенного промпта для генерации плана"""
        prompt = f"""
        Создай персональный план обучения финансовой грамотности для пользователя:
        
        Информация о пользователе:
        - Имя: {profile.first_name if profile and profile.first_name else 'не указано'}
        - Возраст: {profile.age if profile and profile.age else 'не указан'}
        - Уровень опыта: {experience_level}
        - Цели: {', '.join(goals)}
        - Дополнительная информация: {profile.goals if profile and profile.goals else 'не указана'}
        
        Предпочтения: {json.dumps(preferences, ensure_ascii=False) if preferences else 'не указаны'}
        
        Доступные знания в базе:
        """

        for kb in relevant_knowledge[:5]:
            prompt += f"- {kb.title} ({kb.category}): {kb.content[:100]}...\n"

        prompt += """
        
        Создай структурированный план, который будет практичным, достижимым и персонализированным.
        """

        return prompt

    def _build_adaptive_content_prompt(self, lesson: Lesson, user: User, profile: UserProfile,
                                       content_type: str, context_knowledge: List[KnowledgeBase],
                                       user_progress: Dict) -> str:
        """Построение промпта для адаптивного контента"""
        prompt = f"""
        Создай {content_type} для урока "{lesson.title}" адаптированный под пользователя:
        
        Информация об уроке:
        - Название: {lesson.title}
        - Описание: {lesson.description}
        - Категория: {lesson.category}
        - Уровень сложности: {lesson.difficulty_level}
        
        Информация о пользователе:
        - Уровень опыта: {profile.financial_experience if profile else 'не указан'}
        - Завершенных уроков: {user_progress.get('completed_lessons', 0)}
        - Среднее время обучения: {user_progress.get('total_time_spent', 0)} минут
        
        Контекст из базы знаний:
        """

        for kb in context_knowledge:
            prompt += f"- {kb.title}: {kb.content[:150]}...\n"

        prompt += f"""
        
        Создай {content_type}, который будет:
        - Соответствовать уровню пользователя
        - Использовать понятные примеры
        - Включать практические советы
        - Мотивировать к дальнейшему обучению
        """

        return prompt

    def _build_intelligent_validation_prompt(self, quiz: Quiz, user_answer: str, context: str) -> str:
        """Построение промпта для интеллектуальной валидации"""
        return f"""
        Оцени ответ на вопрос по финансовой грамотности:
        
        Контекст: {context}
        
        Вопрос: {quiz.question}
        Тип вопроса: {quiz.question_type}
        Варианты ответов: {json.dumps(quiz.options, ensure_ascii=False) if quiz.options else 'Открытый вопрос'}
        Правильный ответ: {quiz.correct_answer}
        Ответ пользователя: {user_answer}
        
        Дай детальную оценку с конструктивной обратной связью.
        """

    async def _evaluate_content_quality(self, content: str) -> float:
        """Улучшенная оценка качества контента"""
        score = 0.5

        # Базовые проверки
        if len(content) > 200:
            score += 0.1
        if len(content.split()) > 100:
            score += 0.1

        # Проверка на образовательные элементы
        educational_keywords = ['пример', 'например',
                                'важно', 'помните', 'совет', 'рекомендация']
        if any(word in content.lower() for word in educational_keywords):
            score += 0.2

        # Проверка структуры
        if content.count('.') > 5:
            score += 0.1
        if any(marker in content for marker in ['1.', '2.', '•', '-']):
            score += 0.1

        return min(score, 1.0)

    async def _log_ai_interaction(self, interaction_type: str, prompt: str, response: str,
                                  user_id: Optional[int] = None, tokens_used: Optional[int] = None,
                                  processing_time_ms: Optional[int] = None, status: str = "completed",
                                  error_message: Optional[str] = None, metadata: Optional[Dict] = None):
        """Логирование взаимодействий с AI"""
        ai_interaction = AIInteraction(
            user_id=user_id,
            interaction_type=interaction_type,
            prompt=prompt,
            response=response,
            model_version=self.model,
            tokens_used=tokens_used,
            processing_time_ms=processing_time_ms,
            status=status,
            error_message=error_message,
            metadata=metadata
        )

        self.db.add(ai_interaction)
        self.db.commit()
