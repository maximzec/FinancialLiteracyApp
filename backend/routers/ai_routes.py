from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.user import User
from models.ai import PersonalPlan, LessonContent, QuizValidation, AIInteraction
from models.lesson import Lesson, Quiz
from schemas.ai import (
    PersonalPlanCreate, PersonalPlanResponse, LessonContentRequest, LessonContentResponse,
    QuizValidationRequest, QuizValidationResponse, AIInteractionResponse,
    ConceptGenerationRequest, FinancialConceptResponse, AIContentAnalysis,
    PersonalizedRecommendation, LearningPathStep, AITutorResponse
)
from services.ai_service import AIService
from services.vector_service import VectorService
from routers.auth import get_current_user_dependency

router = APIRouter(prefix="/ai", tags=["AI & Machine Learning"])


@router.post("/personal-plan", response_model=PersonalPlanResponse)
async def create_personal_plan(
    plan_request: PersonalPlanCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Создание персонального плана обучения с помощью OpenAI"""
    try:
        ai_service = AIService(db)

        # Проверяем, есть ли уже план у пользователя
        existing_plan = db.query(PersonalPlan).filter(
            PersonalPlan.user_id == current_user.id,
            PersonalPlan.is_active == True
        ).first()

        if existing_plan:
            # Деактивируем старый план
            existing_plan.is_active = False
            db.commit()

        # Генерируем новый план
        personal_plan = await ai_service.generate_personal_plan(
            user_id=current_user.id,
            goals=plan_request.goals,
            experience_level=plan_request.experience_level,
            preferences=plan_request.preferences
        )

        # В фоне векторизуем план для поиска
        background_tasks.add_task(
            vectorize_plan_content,
            personal_plan.id,
            db
        )

        return personal_plan

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании персонального плана: {str(e)}"
        )


@router.get("/personal-plan", response_model=PersonalPlanResponse)
async def get_personal_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение текущего персонального плана пользователя"""
    plan = db.query(PersonalPlan).filter(
        PersonalPlan.user_id == current_user.id,
        PersonalPlan.is_active == True
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У вас нет активного персонального плана"
        )

    return plan


@router.post("/lesson-content", response_model=LessonContentResponse)
async def generate_lesson_content(
    content_request: LessonContentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Генерация адаптивного контента урока с помощью OpenAI"""
    try:
        # Проверяем существование урока
        lesson = db.query(Lesson).filter(
            Lesson.id == content_request.lesson_id).first()
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Урок не найден"
            )

        ai_service = AIService(db)

        lesson_content = await ai_service.generate_adaptive_lesson_content(
            lesson_id=content_request.lesson_id,
            user_id=current_user.id,
            content_type=content_request.content_type
        )

        return lesson_content

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при генерации контента: {str(e)}"
        )


@router.post("/quiz-validation", response_model=QuizValidationResponse)
async def validate_quiz_answer(
    validation_request: QuizValidationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Интеллектуальная валидация ответа на тест с помощью OpenAI"""
    try:
        # Проверяем существование теста
        quiz = db.query(Quiz).filter(
            Quiz.id == validation_request.quiz_id).first()
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тест не найден"
            )

        ai_service = AIService(db)

        validation_result = await ai_service.intelligent_quiz_validation(
            quiz_id=validation_request.quiz_id,
            user_answer=validation_request.user_answer,
            user_id=current_user.id
        )

        return validation_result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при валидации ответа: {str(e)}"
        )


@router.post("/generate-concepts", response_model=List[FinancialConceptResponse])
async def generate_financial_concepts(
    concept_request: ConceptGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Генерация финансовых концепций с помощью OpenAI"""
    try:
        ai_service = AIService(db)

        concepts = await ai_service.generate_financial_concepts(
            category=concept_request.category,
            difficulty_level=concept_request.difficulty_level,
            count=concept_request.count
        )

        return [FinancialConceptResponse(
            id=concept.id,
            term=concept.term,
            definition=concept.definition,
            simple_explanation=concept.simple_explanation,
            examples=concept.examples,
            related_terms=concept.related_terms,
            category=concept.category,
            difficulty_level=concept.difficulty_level,
            usage_count=concept.usage_count,
            created_at=concept.created_at
        ) for concept in concepts]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при генерации концепций: {str(e)}"
        )


@router.post("/tutor-chat", response_model=AITutorResponse)
async def ai_tutor_chat(
    question: str,
    context: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """AI-тьютор для ответов на вопросы по финансовой грамотности"""
    try:
        ai_service = AIService(db)

        # Получаем контекст из базы знаний
        vector_service = VectorService(db)
        search_results = await vector_service.semantic_search(
            query=question,
            user_id=current_user.id,
            limit=3
        )

        # Формируем контекст для AI
        knowledge_context = "\n".join([
            f"- {result['title']}: {result['content'][:200]}..."
            for result in search_results
        ])

        # Создаем промпт для тьютора
        tutor_prompt = f"""
        Вопрос пользователя: {question}
        
        Контекст из базы знаний:
        {knowledge_context}
        
        Дополнительный контекст: {context or 'Не предоставлен'}
        
        Ответь как опытный преподаватель финансовой грамотности. Дай понятный, 
        структурированный ответ с практическими советами.
        """

        response = await ai_service.client.chat.completions.create(
            model=ai_service.model,
            messages=[
                {"role": "system",
                    "content": ai_service._get_financial_expert_system_prompt()},
                {"role": "user", "content": tutor_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        ai_response = response.choices[0].message.content

        # Логируем взаимодействие
        await ai_service._log_ai_interaction(
            user_id=current_user.id,
            interaction_type="tutor_chat",
            prompt=tutor_prompt,
            response=ai_response,
            tokens_used=response.usage.total_tokens
        )

        # Извлекаем связанные концепции из результатов поиска
        related_concepts = [result['title'] for result in search_results]

        return AITutorResponse(
            response_text=ai_response,
            confidence=0.85,  # Можно добавить логику оценки уверенности
            suggested_actions=[
                "Изучите связанные уроки",
                "Попробуйте практические упражнения",
                "Задайте уточняющие вопросы"
            ],
            related_concepts=related_concepts,
            follow_up_questions=[
                "Хотите узнать больше о практическом применении?",
                "Есть ли конкретные примеры, которые вас интересуют?",
                "Нужна ли помощь с расчетами?"
            ]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка AI-тьютора: {str(e)}"
        )


@router.get("/recommendations", response_model=List[PersonalizedRecommendation])
async def get_ai_recommendations(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение персонализированных рекомендаций от AI"""
    try:
        vector_service = VectorService(db)

        recommendations = await vector_service.get_content_recommendations(
            user_id=current_user.id,
            limit=limit
        )

        return [PersonalizedRecommendation(
            content_type=rec['content_type'],
            content_id=rec['content_id'],
            title=rec['title'],
            reason=rec['reason'],
            confidence=rec['score'],
            estimated_time_minutes=rec.get('estimated_time_minutes', 15)
        ) for rec in recommendations]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении рекомендаций: {str(e)}"
        )


@router.post("/analyze-content", response_model=AIContentAnalysis)
async def analyze_content_quality(
    content: str,
    content_type: str = "lesson",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Анализ качества образовательного контента с помощью AI"""
    try:
        ai_service = AIService(db)

        analysis_prompt = f"""
        Проанализируй качество образовательного контента по финансовой грамотности:
        
        Тип контента: {content_type}
        Контент: {content}
        
        Оцени по критериям:
        1. Качество контента (0-1)
        2. Читаемость (0-1) 
        3. Образовательная ценность (0-1)
        4. Уровень вовлеченности (0-1)
        
        Дай рекомендации по улучшению.
        """

        response = await ai_service.client.chat.completions.create(
            model=ai_service.model,
            messages=[
                {"role": "system",
                    "content": "Ты эксперт по оценке образовательного контента."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        # Простая оценка качества (в реальном приложении можно использовать более сложную логику)
        quality_score = await ai_service._evaluate_content_quality(content)

        return AIContentAnalysis(
            content_quality=quality_score,
            readability_score=min(
                1.0, len(content.split()) / 100),  # Простая метрика
            educational_value=0.8,  # Можно добавить более сложную логику
            engagement_level=0.7,
            recommendations=[
                "Добавьте больше практических примеров",
                "Используйте более простой язык",
                "Структурируйте контент с помощью заголовков",
                "Добавьте интерактивные элементы"
            ]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при анализе контента: {str(e)}"
        )


@router.get("/interactions", response_model=List[AIInteractionResponse])
async def get_ai_interactions(
    interaction_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение истории взаимодействий с AI"""
    query = db.query(AIInteraction).filter(
        AIInteraction.user_id == current_user.id)

    if interaction_type:
        query = query.filter(
            AIInteraction.interaction_type == interaction_type)

    interactions = query.order_by(
        AIInteraction.created_at.desc()).offset(skip).limit(limit).all()
    return interactions


@router.get("/learning-path/{plan_id}", response_model=List[LearningPathStep])
async def get_learning_path_steps(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Получение детализированных шагов обучения из персонального плана"""
    plan = db.query(PersonalPlan).filter(
        PersonalPlan.id == plan_id,
        PersonalPlan.user_id == current_user.id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="План обучения не найден"
        )

    # Извлекаем шаги из данных плана
    learning_path = plan.plan_data.get("learning_path", [])

    steps = []
    for i, step_data in enumerate(learning_path):
        steps.append(LearningPathStep(
            step_number=i + 1,
            title=step_data.get("topic", f"Шаг {i + 1}"),
            description=f"Неделя {step_data.get('week', i + 1)}: {step_data.get('topic', '')}",
            estimated_duration_hours=7,  # Примерно час в день
            prerequisites=step_data.get("prerequisites", []),
            learning_objectives=step_data.get("objectives", []),
            resources=step_data.get("resources", []),
            assessment_criteria=step_data.get("activities", [])
        ))

    return steps


# Вспомогательные функции
async def vectorize_plan_content(plan_id: int, db: Session):
    """Фоновая задача для векторизации контента плана"""
    try:
        plan = db.query(PersonalPlan).filter(
            PersonalPlan.id == plan_id).first()
        if plan:
            vector_service = VectorService(db)

            # Создаем текстовое представление плана для векторизации
            plan_text = f"Персональный план обучения. Цели: {', '.join(plan.goals)}. "
            plan_text += f"Уровень: {plan.difficulty_level}. "

            if plan.plan_data.get("learning_path"):
                topics = [step.get("topic", "")
                          for step in plan.plan_data["learning_path"]]
                plan_text += f"Темы: {', '.join(topics)}"

            # Создаем embedding (в реальном приложении можно сохранить в отдельную таблицу)
            embedding = await vector_service.create_embedding(plan_text)

    except Exception as e:
        print(f"Ошибка при векторизации плана {plan_id}: {e}")
