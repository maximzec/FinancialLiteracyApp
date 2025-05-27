# Financial Literacy App

Приложение для обучения финансовой грамотности с поддержкой AI, векторного поиска, полным мониторингом и бизнес-аналитикой.

## 🚀 Возможности

- **Vue.js 3 Frontend** - современный интерфейс с TailwindCSS
- **FastAPI Backend** - высокопроизводительный API
- **AI Integration** - интеграция с OpenAI для персонализированного обучения
- **Vector Search** - семантический поиск с pgvector
- **Gamification** - система достижений и прогресса
- **Real-time Analytics** - аналитика в реальном времени
- **Business Intelligence** - ClickHouse + Grafana для бизнес-аналитики
- **Full Monitoring** - Prometheus + Grafana мониторинг
- **CI/CD Pipeline** - автоматическая сборка и деплой
- **Kubernetes Ready** - готов к продакшн деплою

## 🏗️ Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js 3      │    │    FastAPI      │    │   PostgreSQL    │
│   Frontend      │────│    Backend      │────│   + pgvector    │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │     Redis       │              │
         └──────────────│   Port: 6379    │──────────────┘
                        └─────────────────┘
                                 │
                    ┌─────────────────────────────┐
                    │    Analytics & Monitoring   │
                    │  ClickHouse + Prometheus    │
                    │  Grafana Dashboards         │
                    │  Ports: 8123, 9090, 3001   │
                    └─────────────────────────────┘
```

## 🚀 Быстрый старт

### Локальная разработка

1. **Клонирование репозитория:**
```bash
git clone <repository-url>
cd FinancialLiteracyApp
```

2. **Запуск всего стека:**
```bash
make up
# или
docker-compose up -d
```

3. **Доступ к сервисам:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana (Metrics): http://localhost:3001 (admin/admin)
- Grafana (Analytics): http://localhost:3002 (admin/admin)
- ClickHouse: http://localhost:8123
- Tabix (ClickHouse UI): http://localhost:8124

### Команды разработки

```bash
# Показать все доступные команды
make help

# Запустить сервисы
make up

# Посмотреть логи
make logs

# Запустить тесты
make test

# Создать демо данные для аналитики
make demo-data

# Остановить сервисы
make down
```

## 📊 Аналитическая система

### ClickHouse Database
- **События пользователей** - регистрации, активность, уроки
- **Сессии** - отслеживание пользовательских сессий
- **Бизнес-метрики** - конверсии, retention, revenue
- **Материализованные представления** - для быстрой агрегации

### Типы событий
- `user_registration` - регистрация пользователя
- `lesson_start/complete` - начало/завершение урока
- `ai_chat_message` - взаимодействие с AI
- `page_view` - просмотры страниц
- `payment_completed` - завершенные платежи
- И многие другие...

### Дашборды аналитики
- **Daily Active Users** - ежедневная активность
- **Conversion Funnel** - воронка конверсии
- **Retention Analysis** - анализ удержания
- **Revenue Tracking** - отслеживание доходов
- **Lesson Performance** - эффективность уроков
- **User Engagement** - вовлеченность пользователей

### API аналитики
```bash
# Отправка события
POST /api/v1/analytics/track

# Получение аналитики пользователя
GET /api/v1/analytics/user/{user_id}

# Платформенная аналитика (админы)
GET /api/v1/analytics/platform

# Метрики в реальном времени
GET /api/v1/analytics/real-time

# Экспорт данных (GDPR)
GET /api/v1/analytics/export/user/{user_id}
```

## 📊 Мониторинг

### Метрики приложения
- HTTP запросы и время ответа
- Регистрации пользователей
- Завершения уроков
- AI запросы
- Системные ресурсы

### Дашборды Grafana
- Производительность приложения
- Бизнес метрики
- Системные ресурсы
- Алерты и уведомления

Подробнее: [MONITORING_README.md](MONITORING_README.md)

## 🔄 CI/CD

### GitHub Actions Pipeline
1. **Test** - тестирование backend и frontend
2. **Build** - сборка Docker образов
3. **Push** - публикация в GitHub Container Registry
4. **Deploy** - автоматический деплой в Kubernetes

### Триггеры
- Push в `main` и `develop` ветки
- Pull Request в `main` ветку

## ☸️ Kubernetes

### Деплой в продакшн
```bash
# Применить все манифесты
make k8s-deploy

# Проверить статус
make k8s-status

# Масштабирование
make k8s-scale-backend REPLICAS=5
```

### Мониторинг в Kubernetes
```bash
# Логи приложения
make k8s-logs-backend

# Порт-форвардинг
make k8s-port-forward-prometheus
```

## 🛠️ Технологический стек

### Frontend
- Vue.js 3 с Composition API
- TailwindCSS для стилизации
- Vue Router для навигации
- Axios для HTTP запросов

### Backend
- FastAPI с async/await
- SQLAlchemy 2.0 ORM
- Alembic для миграций
- Pydantic для валидации
- JWT аутентификация

### База данных
- PostgreSQL 15 (основная БД)
- pgvector для векторного поиска
- ClickHouse (аналитическая БД)
- Redis для кэширования

### Аналитика
- ClickHouse для хранения событий
- Grafana для визуализации
- Custom API для бизнес-аналитики
- GDPR-совместимый экспорт данных

### Мониторинг
- Prometheus для метрик
- Grafana для визуализации
- cAdvisor для метрик контейнеров
- Node Exporter для системных метрик

### DevOps
- Docker & Docker Compose
- Kubernetes манифесты
- GitHub Actions CI/CD
- Nginx для фронтенда

## 📁 Структура проекта

```
FinancialLiteracyApp/
├── backend/                 # FastAPI backend
│   ├── routers/            # API роутеры
│   │   └── analytics.py    # Аналитические API
│   ├── models/             # SQLAlchemy модели
│   ├── schemas/            # Pydantic схемы
│   │   └── analytics.py    # Схемы аналитики
│   ├── services/           # Бизнес логика
│   ├── analytics.py        # ClickHouse интеграция
│   ├── metrics.py          # Prometheus метрики
│   └── main.py             # Точка входа
├── ui/                     # Vue.js frontend
│   ├── src/
│   │   ├── components/     # Vue компоненты
│   │   ├── views/          # Страницы
│   │   └── router/         # Маршрутизация
│   ├── Dockerfile          # Docker образ
│   └── nginx.conf          # Nginx конфигурация
├── k8s/                    # Kubernetes манифесты
│   ├── namespace.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── prometheus.yaml
├── monitoring/             # Конфигурация мониторинга
│   ├── prometheus/         # Prometheus конфиги
│   ├── grafana/           # Grafana дашборды (метрики)
│   ├── grafana-analytics/ # Grafana дашборды (аналитика)
│   └── clickhouse/        # ClickHouse конфигурация
├── .github/workflows/      # CI/CD pipeline
├── docker-compose.yml      # Локальная разработка
├── Makefile               # Команды управления
└── README.md
```

## 🔧 Конфигурация

### Переменные окружения

```bash
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_DATABASE=analytics
OPENAI_API_KEY=your-openai-key
JWT_SECRET_KEY=your-secret-key

# Monitoring
PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus
```

### Секреты для CI/CD

```bash
# GitHub Secrets
KUBE_CONFIG=<base64-encoded-kubeconfig>
OPENAI_API_KEY=<your-openai-key>
```

## 🧪 Тестирование

```bash
# Все тесты
make test

# Только backend
make test-backend

# Только frontend
make test-frontend

# Линтинг
make lint
```

## 📈 Производительность

- **Backend**: до 1000 RPS на одном инстансе
- **Frontend**: статические файлы через Nginx
- **База данных**: оптимизированные индексы
- **Аналитика**: ClickHouse для быстрых агрегаций
- **Кэширование**: Redis для частых запросов
- **Мониторинг**: метрики в реальном времени

## 🔒 Безопасность

- JWT токены для аутентификации
- CORS настройки
- Rate limiting
- SQL injection защита
- XSS защита
- GDPR compliance для аналитики
- HTTPS в продакшене

## 📊 Бизнес-аналитика

### Ключевые метрики
- **DAU/MAU** - ежедневные/месячные активные пользователи
- **Retention Rate** - процент удержания пользователей
- **Conversion Funnel** - воронка конверсии
- **LTV** - пожизненная ценность пользователя
- **Lesson Completion Rate** - процент завершения уроков
- **AI Engagement** - взаимодействие с AI

### Отчеты
- Еженедельные отчеты по активности
- Ежемесячные бизнес-отчеты
- Анализ эффективности контента
- Когортный анализ пользователей

### GDPR Compliance
- Экспорт пользовательских данных
- Удаление данных по запросу
- Анонимизация старых данных
- Настройки приватности

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature ветку
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License

## 📞 Поддержка

Для вопросов и предложений создавайте Issues в GitHub репозитории.