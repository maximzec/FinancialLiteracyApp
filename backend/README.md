# 🏦 Financial Literacy App - Backend

Полнофункциональный backend для приложения финансовой грамотности с интеграцией OpenAI, векторным поиском и геймификацией.

## 🚀 Основные возможности

### 🤖 Интеграция с OpenAI
- **Персональные планы обучения** - AI создает индивидуальные планы на основе целей и опыта пользователя
- **Адаптивный контент** - Генерация контента уроков под конкретного пользователя
- **Интеллектуальная валидация тестов** - AI оценивает ответы с детальной обратной связью
- **AI-тьютор** - Ответы на вопросы пользователей с контекстом из базы знаний
- **Генерация финансовых концепций** - Автоматическое создание терминов и определений
- **Анализ качества контента** - Оценка образовательных материалов

### 🔍 Векторный поиск и рекомендации
- **PostgreSQL + pgvector** - Векторная база данных для семантического поиска
- **Embeddings OpenAI** - Векторизация контента для точного поиска
- **Персонализированные рекомендации** - AI-рекомендации на основе поведения пользователя
- **Семантический поиск** - Поиск по смыслу, а не только по ключевым словам

### 🎮 Геймификация
- **Система коинов** - Награды за прохождение уроков и активность
- **Челленджи** - Персональные и групповые вызовы
- **Массовые события** - Соревнования между пользователями
- **Достижения и лидерборды** - Мотивация через соревновательность

### 📚 Система обучения
- **Структурированные уроки** - Прогрессивное обучение с отслеживанием прогресса
- **Интерактивные тесты** - Проверка знаний с AI-валидацией
- **База знаний** - Централизованное хранение финансовых концепций
- **Отслеживание прогресса** - Детальная аналитика обучения

### ⚡ Технологический стек
- **FastAPI** - Современный веб-фреймворк
- **PostgreSQL + pgvector** - Основная и векторная БД
- **Redis** - Кеширование и сессии
- **OpenAI API** - GPT-4 и embeddings
- **Apache Kafka** - Event-driven архитектура
- **Kubernetes** - Контейнеризация и оркестрация

## 📁 Структура проекта

```
backend/
├── 📁 models/              # SQLAlchemy модели
│   ├── user.py            # Пользователи и профили
│   ├── lesson.py          # Уроки и прогресс
│   ├── gamification.py    # Геймификация
│   ├── ai.py              # AI-функции
│   └── vector_data.py     # Векторные данные
├── 📁 schemas/            # Pydantic схемы
│   ├── user.py           # Схемы пользователей
│   ├── lesson.py         # Схемы уроков
│   ├── gamification.py   # Схемы геймификации
│   ├── ai.py             # Схемы AI
│   └── vector_data.py    # Схемы векторных данных
├── 📁 routers/           # API роутеры
│   ├── auth.py          # Авторизация
│   ├── lessons.py       # Уроки
│   ├── gamification.py  # Геймификация
│   ├── ai_routes.py     # AI функции
│   ├── search.py        # Поиск и рекомендации
│   └── users.py         # Пользователи
├── 📁 services/         # Бизнес-логика
│   ├── auth_service.py  # Авторизация
│   ├── ai_service.py    # OpenAI интеграция
│   ├── vector_service.py # Векторный поиск
│   └── kafka_service.py # Event processing
├── 📁 k8s/              # Kubernetes конфигурации
├── 📁 examples/         # Демонстрации
│   └── openai_integration_demo.py
├── config.py            # Конфигурация
├── database.py          # Подключение к БД
├── main.py              # Главный файл
└── requirements.txt     # Зависимости
```

## 🛠 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd FinancialLiteracyApp/backend
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
```bash
# .env файл
DATABASE_URL=postgresql://user:password@localhost/financial_app
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET_KEY=your_secret_key
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

### 4. Инициализация базы данных
```bash
# Создание таблиц и векторных индексов
python -c "
import asyncio
from database import init_db, create_vector_index
asyncio.run(init_db())
asyncio.run(create_vector_index())
"
```

### 5. Запуск приложения
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🤖 Демонстрация OpenAI интеграции

Запустите демонстрацию всех AI возможностей:

```bash
python -m examples.openai_integration_demo
```

Демонстрация покажет:
- ✅ Генерацию персональных планов обучения
- ✅ Создание адаптивного контента уроков
- ✅ Интеллектуальную валидацию тестов
- ✅ Работу AI-тьютора
- ✅ Генерацию финансовых концепций
- ✅ Анализ качества контента
- ✅ Создание векторных представлений

## 📊 API Endpoints

### 🔐 Авторизация (`/api/v1/auth`)
- `POST /register` - Регистрация пользователя
- `POST /login` - Авторизация
- `POST /refresh` - Обновление токена
- `GET /me` - Получение профиля

### 📚 Уроки (`/api/v1/lessons`)
- `GET /` - Список уроков
- `GET /{id}` - Конкретный урок
- `POST /{id}/start` - Начать урок
- `PUT /{id}/progress` - Обновить прогресс
- `GET /{id}/quiz` - Тесты урока
- `POST /quiz/{id}/answer` - Ответить на тест

### 🎮 Геймификация (`/api/v1/gamification`)
- `GET /challenges` - Список челленджей
- `POST /challenges/{id}/join` - Присоединиться к челленджу
- `GET /my-challenges` - Мои челленджи
- `GET /coins` - Баланс коинов
- `GET /leaderboard` - Таблица лидеров
- `GET /stats` - Статистика геймификации

### 🤖 AI функции (`/api/v1/ai`)
- `POST /personal-plan` - Создать персональный план
- `GET /personal-plan` - Получить план
- `POST /lesson-content` - Генерация контента урока
- `POST /quiz-validation` - Валидация ответа
- `POST /tutor-chat` - Чат с AI-тьютором
- `GET /recommendations` - AI-рекомендации
- `POST /generate-concepts` - Генерация концепций
- `POST /analyze-content` - Анализ контента

### 🔍 Поиск (`/api/v1/search`)
- `POST /semantic` - Семантический поиск
- `GET /recommendations` - Рекомендации
- `GET /concepts/{concept}` - Связанные концепции
- `POST /knowledge-base` - Добавить знания
- `GET /trending` - Популярный контент

### 👤 Пользователи (`/api/v1/users`)
- `GET /me` - Профиль пользователя
- `POST /profile` - Создать профиль
- `PUT /profile` - Обновить профиль
- `GET /stats` - Статистика обучения
- `GET /dashboard` - Дашборд пользователя
- `GET /achievements` - Достижения

## 🔧 Конфигурация

### OpenAI настройки
```python
# config.py
OPENAI_API_KEY = "your_api_key"
OPENAI_MODEL = "gpt-4"  # или gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
```

### Векторная база данных
```python
# Автоматическое создание pgvector extension
# и HNSW индексов для быстрого поиска
```

### Kafka события
```python
# Автоматическая отправка событий:
# - user_registered
# - lesson_completed
# - challenge_joined
# - quiz_answered
```

## 🚀 Деплой в Kubernetes

```bash
# Применение конфигураций
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml

# Проверка статуса
kubectl get pods -n financial-app
```

## 📈 Мониторинг и логирование

- **Prometheus метрики** - Автоматический сбор метрик
- **Структурированное логирование** - JSON логи для анализа
- **Health checks** - `/health` и `/ready` endpoints
- **AI взаимодействия** - Полное логирование запросов к OpenAI

## 🔒 Безопасность

- **JWT токены** - Безопасная авторизация
- **Хеширование паролей** - bcrypt
- **Валидация данных** - Pydantic схемы
- **Rate limiting** - Защита от злоупотреблений
- **CORS настройки** - Контроль доступа

## 🧪 Тестирование

```bash
# Запуск тестов
pytest

# Тестирование API
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/api/v1/lessons
```

## 📝 Примеры использования

### Создание персонального плана
```python
import httpx

response = httpx.post("http://localhost:8000/api/v1/ai/personal-plan", 
    json={
        "goals": ["Научиться инвестировать", "Создать финансовую подушку"],
        "experience_level": "beginner",
        "preferences": {"learning_style": "visual"}
    },
    headers={"Authorization": "Bearer your_token"}
)
```

### Семантический поиск
```python
response = httpx.post("http://localhost:8000/api/v1/search/semantic",
    json={
        "query": "Как начать инвестировать?",
        "limit": 5
    },
    headers={"Authorization": "Bearer your_token"}
)
```

### AI-тьютор
```python
response = httpx.post("http://localhost:8000/api/v1/ai/tutor-chat",
    params={"question": "Что такое диверсификация?"},
    headers={"Authorization": "Bearer your_token"}
)
```

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License - см. файл LICENSE

## 🆘 Поддержка

- 📧 Email: support@financialapp.com
- 💬 Telegram: @financial_app_support
- 📖 Документация: [docs.financialapp.com](https://docs.financialapp.com)

---

**Примечание**: Этот проект является демонстрационным псевдокодом для показа архитектуры и возможностей интеграции с OpenAI. Для продакшена требуется дополнительная настройка безопасности, тестирование и оптимизация. 