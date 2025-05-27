.PHONY: help build up down logs test clean deploy k8s-deploy k8s-clean

# Переменные
DOCKER_COMPOSE = docker-compose
KUBECTL = kubectl
NAMESPACE = financial-literacy

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Локальная разработка
build: ## Собрать Docker образы
	$(DOCKER_COMPOSE) build

up: ## Запустить все сервисы
	$(DOCKER_COMPOSE) up -d

down: ## Остановить все сервисы
	$(DOCKER_COMPOSE) down

logs: ## Показать логи всех сервисов
	$(DOCKER_COMPOSE) logs -f

logs-backend: ## Показать логи backend
	$(DOCKER_COMPOSE) logs -f backend

logs-frontend: ## Показать логи frontend
	$(DOCKER_COMPOSE) logs -f frontend

logs-prometheus: ## Показать логи Prometheus
	$(DOCKER_COMPOSE) logs -f prometheus

logs-grafana: ## Показать логи Grafana
	$(DOCKER_COMPOSE) logs -f grafana

logs-clickhouse: ## Показать логи ClickHouse
	$(DOCKER_COMPOSE) logs -f clickhouse

logs-analytics: ## Показать логи Grafana Analytics
	$(DOCKER_COMPOSE) logs -f grafana-analytics

# Тестирование
test: ## Запустить тесты
	cd backend && python -m pytest
	cd ui && npm test

test-backend: ## Запустить тесты backend
	cd backend && python -m pytest

test-frontend: ## Запустить тесты frontend
	cd ui && npm test

lint: ## Проверить код линтером
	cd backend && flake8 .
	cd ui && npm run lint

# Очистка
clean: ## Очистить Docker ресурсы
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f

clean-all: ## Полная очистка Docker
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -af
	docker volume prune -f

# Kubernetes
k8s-deploy: ## Деплой в Kubernetes
	$(KUBECTL) apply -f k8s/namespace.yaml
	$(KUBECTL) apply -f k8s/prometheus-rules.yaml
	$(KUBECTL) apply -f k8s/prometheus.yaml
	$(KUBECTL) apply -f k8s/backend-deployment.yaml
	$(KUBECTL) apply -f k8s/frontend-deployment.yaml

k8s-clean: ## Удалить из Kubernetes
	$(KUBECTL) delete -f k8s/ --ignore-not-found=true

k8s-status: ## Проверить статус в Kubernetes
	$(KUBECTL) get all -n $(NAMESPACE)

k8s-logs-backend: ## Логи backend в Kubernetes
	$(KUBECTL) logs -f deployment/financial-literacy-backend -n $(NAMESPACE)

k8s-logs-frontend: ## Логи frontend в Kubernetes
	$(KUBECTL) logs -f deployment/financial-literacy-frontend -n $(NAMESPACE)

k8s-logs-prometheus: ## Логи Prometheus в Kubernetes
	$(KUBECTL) logs -f deployment/prometheus -n $(NAMESPACE)

# Мониторинг
metrics: ## Показать метрики backend
	curl http://localhost:8000/metrics

health: ## Проверить health check
	curl http://localhost:8000/health

prometheus-reload: ## Перезагрузить конфигурацию Prometheus
	curl -X POST http://localhost:9090/-/reload

# Аналитика
analytics-query: ## Выполнить тестовый запрос к ClickHouse
	curl "http://localhost:8123/?query=SELECT%20count()%20FROM%20analytics.events"

analytics-tables: ## Показать таблицы в ClickHouse
	curl "http://localhost:8123/?query=SHOW%20TABLES%20FROM%20analytics"

analytics-events: ## Показать последние события
	curl "http://localhost:8123/?query=SELECT%20*%20FROM%20analytics.events%20ORDER%20BY%20timestamp%20DESC%20LIMIT%2010"

analytics-users: ## Показать статистику пользователей
	curl "http://localhost:8123/?query=SELECT%20count()%20as%20total_users%20FROM%20analytics.users"

# Порт-форвардинг для Kubernetes
k8s-port-forward-backend: ## Порт-форвардинг backend
	$(KUBECTL) port-forward svc/financial-literacy-backend-service 8000:8000 -n $(NAMESPACE)

k8s-port-forward-frontend: ## Порт-форвардинг frontend
	$(KUBECTL) port-forward svc/financial-literacy-frontend-service 3000:80 -n $(NAMESPACE)

k8s-port-forward-prometheus: ## Порт-форвардинг Prometheus
	$(KUBECTL) port-forward svc/prometheus-service 9090:9090 -n $(NAMESPACE)

# Масштабирование
k8s-scale-backend: ## Масштабировать backend (использование: make k8s-scale-backend REPLICAS=5)
	$(KUBECTL) scale deployment financial-literacy-backend --replicas=$(REPLICAS) -n $(NAMESPACE)

k8s-scale-frontend: ## Масштабировать frontend (использование: make k8s-scale-frontend REPLICAS=3)
	$(KUBECTL) scale deployment financial-literacy-frontend --replicas=$(REPLICAS) -n $(NAMESPACE)

# Разработка
dev-backend: ## Запустить backend в режиме разработки
	cd backend && python main.py

dev-frontend: ## Запустить frontend в режиме разработки
	cd ui && npm run serve

install-backend: ## Установить зависимости backend
	cd backend && pip install -r requirements.txt

install-frontend: ## Установить зависимости frontend
	cd ui && npm install

# Мониторинг URLs
urls: ## Показать URLs сервисов
	@echo "Локальные сервисы:"
	@echo "Frontend:           http://localhost:3000"
	@echo "Backend:            http://localhost:8000"
	@echo "Prometheus:         http://localhost:9090"
	@echo "Grafana (Metrics):  http://localhost:3001 (admin/admin)"
	@echo "Grafana (Analytics): http://localhost:3002 (admin/admin)"
	@echo "ClickHouse:         http://localhost:8123"
	@echo "Tabix (ClickHouse): http://localhost:8124"
	@echo "cAdvisor:           http://localhost:8080"
	@echo ""
	@echo "API endpoints:"
	@echo "Health:             http://localhost:8000/health"
	@echo "Metrics:            http://localhost:8000/metrics"
	@echo "Analytics API:      http://localhost:8000/api/v1/analytics"
	@echo "Docs:               http://localhost:8000/docs"

# Демо данные
demo-data: ## Создать демо данные для аналитики
	@echo "Создание демо данных для аналитики..."
	curl -X POST "http://localhost:8000/api/v1/analytics/track" \
		-H "Content-Type: application/json" \
		-d '{"event_type": "user_registration", "properties": {"source": "demo"}}'
	curl -X POST "http://localhost:8000/api/v1/analytics/lesson/start" \
		-H "Content-Type: application/json" \
		-d '{"lesson_id": "demo_lesson_1"}'
	@echo "Демо данные созданы!"

# Бэкап и восстановление
backup-analytics: ## Создать бэкап аналитических данных
	@echo "Создание бэкапа ClickHouse..."
	docker exec financial-literacy-clickhouse clickhouse-client --query="BACKUP DATABASE analytics TO Disk('backups', 'analytics_backup_$(shell date +%Y%m%d_%H%M%S)')"

restore-analytics: ## Восстановить аналитические данные (использование: make restore-analytics BACKUP_NAME=analytics_backup_20231201_120000)
	@echo "Восстановление бэкапа ClickHouse..."
	docker exec financial-literacy-clickhouse clickhouse-client --query="RESTORE DATABASE analytics FROM Disk('backups', '$(BACKUP_NAME)')" 