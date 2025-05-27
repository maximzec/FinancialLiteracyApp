# Мониторинг и CI/CD для Financial Literacy App

## Обзор

Этот проект включает полную систему мониторинга и CI/CD для приложения финансовой грамотности:

- **CI/CD Pipeline** - автоматическая сборка и деплой через GitHub Actions
- **Prometheus** - сбор метрик приложения и системы
- **Grafana** - визуализация метрик и дашборды
- **Kubernetes** - оркестрация контейнеров в продакшене
- **Docker Compose** - локальная разработка

## Архитектура мониторинга

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Prometheus    │
│   (Vue.js)      │────│   (FastAPI)     │────│                 │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 9090    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │    Grafana      │
                    │   Port: 3001    │
                    └─────────────────┘
```

## Быстрый старт

### Локальная разработка

1. **Запуск всего стека:**
```bash
docker-compose up -d
```

2. **Доступ к сервисам:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)

### Продакшн деплой

1. **Настройка секретов GitHub:**
```bash
# Добавьте в GitHub Secrets:
KUBE_CONFIG=<base64-encoded-kubeconfig>
```

2. **Деплой в Kubernetes:**
```bash
# Применение манифестов
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/prometheus-rules.yaml
kubectl apply -f k8s/prometheus.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```

## Метрики приложения

### HTTP метрики
- `http_requests_total` - общее количество HTTP запросов
- `http_request_duration_seconds` - время ответа HTTP запросов

### Бизнес метрики
- `user_registrations_total` - количество регистраций пользователей
- `lesson_completions_total` - количество завершенных уроков
- `ai_requests_total` - количество AI запросов
- `ai_request_duration_seconds` - время выполнения AI запросов

### Системные метрики
- `active_users` - количество активных пользователей
- `database_connections_active` - активные подключения к БД
- `cpu_usage_percent` - использование CPU
- `memory_usage_bytes` - использование памяти
- `disk_usage_percent` - использование диска

## Алерты

Настроены следующие алерты:

1. **HighErrorRate** - высокий уровень ошибок (>10%)
2. **HighResponseTime** - высокое время ответа (>1s)
3. **HighCPUUsage** - высокое использование CPU (>80%)
4. **HighMemoryUsage** - высокое использование памяти (>2GB)
5. **ServiceDown** - сервис недоступен
6. **DatabaseConnectionIssues** - проблемы с БД (>50 соединений)
7. **AIRequestFailures** - сбои AI запросов

## CI/CD Pipeline

### Этапы pipeline:

1. **Test Backend** - тестирование Python кода
2. **Test Frontend** - линтинг и сборка Vue.js
3. **Build and Push** - сборка Docker образов
4. **Deploy** - деплой в Kubernetes (только main ветка)

### Триггеры:
- Push в ветки `main` и `develop`
- Pull Request в ветку `main`

### Образы:
- Backend: `ghcr.io/{owner}/{repo}/backend`
- Frontend: `ghcr.io/{owner}/{repo}/frontend`

## Grafana дашборды

### Основной дашборд включает:

1. **HTTP Requests per Second** - RPS по эндпоинтам
2. **Response Time (95th percentile)** - время ответа
3. **Error Rate** - процент ошибок
4. **Active Users** - активные пользователи
5. **CPU Usage** - использование процессора
6. **Memory Usage** - использование памяти
7. **AI Requests** - AI запросы по типам
8. **Lesson Completions** - завершения уроков

## Использование метрик в коде

### Backend (Python)

```python
from metrics import track_user_registration, track_lesson_completion, track_ai_request

# Отслеживание регистрации пользователя
@track_user_registration()
async def register_user(user_data):
    # логика регистрации
    pass

# Отслеживание завершения урока
@track_lesson_completion("lesson_1")
async def complete_lesson(lesson_id):
    # логика завершения урока
    pass

# Отслеживание AI запроса
@track_ai_request("chat_completion")
async def ai_chat(message):
    # логика AI чата
    pass
```

## Мониторинг в Kubernetes

### Проверка статуса:
```bash
# Проверка подов
kubectl get pods -n financial-literacy

# Проверка сервисов
kubectl get services -n financial-literacy

# Логи приложения
kubectl logs -f deployment/financial-literacy-backend -n financial-literacy

# Метрики Prometheus
kubectl port-forward svc/prometheus-service 9090:9090 -n financial-literacy
```

### Масштабирование:
```bash
# Увеличение реплик backend
kubectl scale deployment financial-literacy-backend --replicas=5 -n financial-literacy

# Увеличение реплик frontend
kubectl scale deployment financial-literacy-frontend --replicas=3 -n financial-literacy
```

## Troubleshooting

### Общие проблемы:

1. **Метрики не собираются:**
   - Проверьте аннотации `prometheus.io/scrape: "true"`
   - Убедитесь, что endpoint `/metrics` доступен

2. **Grafana не показывает данные:**
   - Проверьте подключение к Prometheus
   - Убедитесь, что метрики существуют в Prometheus

3. **CI/CD не работает:**
   - Проверьте секреты GitHub
   - Убедитесь в правильности KUBE_CONFIG

4. **Высокое использование ресурсов:**
   - Проверьте лимиты ресурсов в Kubernetes
   - Оптимизируйте запросы к БД

### Полезные команды:

```bash
# Проверка метрик напрямую
curl http://localhost:8000/metrics

# Проверка health check
curl http://localhost:8000/health

# Перезагрузка конфигурации Prometheus
curl -X POST http://localhost:9090/-/reload

# Экспорт дашборда Grafana
curl -H "Authorization: Bearer <token>" \
  http://localhost:3001/api/dashboards/uid/financial-literacy-main
```

## Безопасность

1. **Секреты** хранятся в Kubernetes Secrets
2. **RBAC** настроен для Prometheus
3. **Network Policies** ограничивают трафик
4. **TLS** используется для внешних соединений

## Производительность

### Рекомендации:

1. **Retention** метрик - 200 часов
2. **Scrape interval** - 15 секунд
3. **Evaluation interval** - 15 секунд
4. **Storage** - 10GB для Prometheus

### Оптимизация:

1. Используйте лейблы разумно
2. Избегайте высококардинальных метрик
3. Настройте правильные лимиты ресурсов
4. Мониторьте сам мониторинг

## Дальнейшее развитие

1. **Alertmanager** для уведомлений
2. **Jaeger** для трейсинга
3. **ELK Stack** для логов
4. **Service Mesh** (Istio) для микросервисов
5. **GitOps** с ArgoCD 