"""
Демонстрация интеграции с OpenAI API в приложении финансовой грамотности

Этот файл показывает, как используется OpenAI в различных частях приложения.
Все функции являются рабочими примерами, но требуют настройки API ключа.
"""

import asyncio
import json
from typing import List, Dict, Any
import openai
from config import settings

# Инициализация клиента OpenAI
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


async def demo_personal_plan_generation():
    """Демонстрация генерации персонального плана обучения"""
    print("🎯 Демонстрация: Генерация персонального плана обучения")
    print("-" * 60)

    user_goals = ["Научиться инвестировать",
                  "Создать финансовую подушку", "Планировать пенсию"]
    experience_level = "beginner"

    prompt = f"""
    Создай персональный план обучения финансовой грамотности для пользователя:
    
    Цели: {', '.join(user_goals)}
    Уровень опыта: {experience_level}
    
    Создай структурированный план на 12 недель с конкретными шагами и ресурсами.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты эксперт по финансовой грамотности и персональному планированию."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            functions=[{
                "name": "generate_learning_plan",
                "description": "Генерирует персональный план обучения",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "duration_weeks": {"type": "integer"},
                        "learning_path": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "week": {"type": "integer"},
                                    "topic": {"type": "string"},
                                    "objectives": {"type": "array", "items": {"type": "string"}},
                                    "activities": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        },
                        "milestones": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }],
            function_call={"name": "generate_learning_plan"}
        )

        plan_data = json.loads(
            response.choices[0].message.function_call.arguments)

        print(f"✅ План создан на {plan_data['duration_weeks']} недель")
        print(f"📚 Количество этапов: {len(plan_data['learning_path'])}")
        print(f"🎯 Ключевые вехи: {len(plan_data['milestones'])}")

        # Показываем первые 3 недели
        for week_data in plan_data['learning_path'][:3]:
            print(f"\n📅 Неделя {week_data['week']}: {week_data['topic']}")
            for objective in week_data['objectives'][:2]:
                print(f"   • {objective}")

        print(f"\n💰 Использовано токенов: {response.usage.total_tokens}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def demo_adaptive_content_generation():
    """Демонстрация генерации адаптивного контента урока"""
    print("\n📝 Демонстрация: Генерация адаптивного контента")
    print("-" * 60)

    lesson_topic = "Основы инвестирования"
    user_level = "beginner"

    prompt = f"""
    Создай образовательный контент для урока "{lesson_topic}" 
    адаптированный для уровня "{user_level}".
    
    Контент должен быть понятным, структурированным и включать практические примеры.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                    "content": "Ты опытный преподаватель финансовой грамотности."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=1500,
            functions=[{
                "name": "generate_educational_content",
                "description": "Генерирует образовательный контент",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "key_points": {"type": "array", "items": {"type": "string"}},
                        "examples": {"type": "array", "items": {"type": "string"}},
                        "practical_tips": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }],
            function_call={"name": "generate_educational_content"}
        )

        content_data = json.loads(
            response.choices[0].message.function_call.arguments)

        print(f"✅ Контент создан для урока: {lesson_topic}")
        print(f"📖 Длина контента: {len(content_data['content'])} символов")
        print(f"🔑 Ключевых моментов: {len(content_data['key_points'])}")
        print(f"💡 Практических советов: {len(content_data['practical_tips'])}")

        # Показываем ключевые моменты
        print("\n🔑 Ключевые моменты:")
        for point in content_data['key_points'][:3]:
            print(f"   • {point}")

        print(f"\n💰 Использовано токенов: {response.usage.total_tokens}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def demo_intelligent_quiz_validation():
    """Демонстрация интеллектуальной валидации ответов на тесты"""
    print("\n🧠 Демонстрация: Интеллектуальная валидация тестов")
    print("-" * 60)

    question = "Что такое диверсификация инвестиций?"
    correct_answer = "Распределение инвестиций между разными активами для снижения риска"
    user_answer = "Это когда покупаешь разные акции, чтобы не потерять все деньги сразу"

    prompt = f"""
    Оцени ответ на вопрос по финансовой грамотности:
    
    Вопрос: {question}
    Правильный ответ: {correct_answer}
    Ответ пользователя: {user_answer}
    
    Дай детальную оценку с конструктивной обратной связью.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                    "content": "Ты эксперт по оценке знаний в области финансов."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800,
            functions=[{
                "name": "validate_quiz_answer",
                "description": "Валидирует ответ на тест",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_correct": {"type": "boolean"},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "detailed_feedback": {"type": "string"},
                        "improvement_suggestions": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }],
            function_call={"name": "validate_quiz_answer"}
        )

        validation_result = json.loads(
            response.choices[0].message.function_call.arguments)

        print(f"✅ Ответ оценен")
        print(
            f"🎯 Правильность: {'Да' if validation_result['is_correct'] else 'Нет'}")
        print(f"📊 Уверенность: {validation_result['confidence']:.2f}")
        print(
            f"💬 Обратная связь: {validation_result['detailed_feedback'][:100]}...")

        if validation_result['improvement_suggestions']:
            print("\n💡 Рекомендации:")
            for suggestion in validation_result['improvement_suggestions'][:2]:
                print(f"   • {suggestion}")

        print(f"\n💰 Использовано токенов: {response.usage.total_tokens}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def demo_ai_tutor_chat():
    """Демонстрация AI-тьютора для ответов на вопросы"""
    print("\n🤖 Демонстрация: AI-тьютор")
    print("-" * 60)

    user_question = "Как начать инвестировать с небольшой суммой?"

    prompt = f"""
    Вопрос пользователя: {user_question}
    
    Ответь как опытный преподаватель финансовой грамотности. 
    Дай понятный, структурированный ответ с практическими советами.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты AI-тьютор по финансовой грамотности. Отвечай понятно и практично."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        ai_response = response.choices[0].message.content

        print(f"✅ Ответ получен")
        print(f"📝 Длина ответа: {len(ai_response)} символов")
        print(f"🎯 Вопрос: {user_question}")
        print(f"🤖 Ответ: {ai_response[:200]}...")

        print(f"\n💰 Использовано токенов: {response.usage.total_tokens}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def demo_financial_concepts_generation():
    """Демонстрация генерации финансовых концепций"""
    print("\n📚 Демонстрация: Генерация финансовых концепций")
    print("-" * 60)

    category = "инвестирование"
    difficulty_level = "beginner"

    prompt = f"""
    Сгенерируй 5 важных финансовых концепций для категории "{category}" 
    уровня сложности "{difficulty_level}". 
    
    Для каждой концепции предоставь:
    - Термин
    - Определение
    - Простое объяснение
    - Пример использования
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты эксперт по финансовой терминологии."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            functions=[{
                "name": "generate_financial_concepts",
                "description": "Генерирует финансовые концепции",
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
                                    "example": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }],
            function_call={"name": "generate_financial_concepts"}
        )

        concepts_data = json.loads(
            response.choices[0].message.function_call.arguments)

        print(f"✅ Создано концепций: {len(concepts_data['concepts'])}")

        # Показываем первые 2 концепции
        for i, concept in enumerate(concepts_data['concepts'][:2], 1):
            print(f"\n📖 Концепция {i}: {concept['term']}")
            print(f"   Определение: {concept['definition'][:80]}...")
            print(
                f"   Простое объяснение: {concept['simple_explanation'][:80]}...")

        print(f"\n💰 Использовано токенов: {response.usage.total_tokens}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def demo_content_analysis():
    """Демонстрация анализа качества контента"""
    print("\n🔍 Демонстрация: Анализ качества контента")
    print("-" * 60)

    content = """
    Инвестирование - это процесс размещения денег с целью получения прибыли. 
    Существует много видов инвестиций: акции, облигации, недвижимость. 
    Важно помнить о диверсификации и не вкладывать все деньги в один актив.
    """

    prompt = f"""
    Проанализируй качество образовательного контента по финансовой грамотности:
    
    Контент: {content}
    
    Оцени по критериям:
    1. Качество контента (0-1)
    2. Читаемость (0-1)
    3. Образовательная ценность (0-1)
    4. Уровень вовлеченности (0-1)
    
    Дай рекомендации по улучшению.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                    "content": "Ты эксперт по оценке образовательного контента."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        analysis = response.choices[0].message.content

        print(f"✅ Анализ завершен")
        print(f"📊 Результат анализа: {analysis[:150]}...")

        # Простая оценка качества
        quality_score = min(1.0, len(content.split()) / 50)  # Базовая метрика
        print(f"🎯 Оценка качества: {quality_score:.2f}")

        print(f"\n💰 Использовано токенов: {response.usage.total_tokens}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def demo_embeddings_creation():
    """Демонстрация создания векторных представлений"""
    print("\n🔢 Демонстрация: Создание embeddings")
    print("-" * 60)

    texts = [
        "Диверсификация помогает снизить инвестиционные риски",
        "Сложный процент - восьмое чудо света",
        "Финансовая подушка должна покрывать 3-6 месяцев расходов"
    ]

    try:
        for i, text in enumerate(texts, 1):
            response = await client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )

            embedding = response.data[0].embedding

            print(f"✅ Embedding {i} создан")
            print(f"📝 Текст: {text}")
            print(f"🔢 Размерность: {len(embedding)}")
            print(f"📊 Первые 5 значений: {embedding[:5]}")
            print(f"💰 Токенов использовано: {response.usage.total_tokens}")
            print()

    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def main():
    """Запуск всех демонстраций"""
    print("🚀 Демонстрация интеграции с OpenAI API")
    print("=" * 60)

    demos = [
        demo_personal_plan_generation,
        demo_adaptive_content_generation,
        demo_intelligent_quiz_validation,
        demo_ai_tutor_chat,
        demo_financial_concepts_generation,
        demo_content_analysis,
        demo_embeddings_creation
    ]

    for demo in demos:
        try:
            await demo()
            await asyncio.sleep(1)  # Пауза между запросами
        except Exception as e:
            print(f"❌ Ошибка в демонстрации: {e}")

    print("\n🎉 Все демонстрации завершены!")
    print("\n📋 Возможности OpenAI в приложении:")
    print("   • Персональные планы обучения")
    print("   • Адаптивный контент уроков")
    print("   • Интеллектуальная валидация тестов")
    print("   • AI-тьютор для вопросов")
    print("   • Генерация финансовых концепций")
    print("   • Анализ качества контента")
    print("   • Векторный поиск и рекомендации")


if __name__ == "__main__":
    # Для запуска демонстрации:
    # python -m examples.openai_integration_demo
    asyncio.run(main())
