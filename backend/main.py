from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from config import settings
from database import init_db, create_vector_index
from routers import auth, lessons, gamification, ai_routes, search, users, analytics
from services.kafka_service import KafkaService
from metrics import PrometheusMiddleware, get_metrics, CONTENT_TYPE_LATEST
from analytics import analytics as analytics_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print("Database initialized")

    # Создаем векторные индексы
    await create_vector_index()
    print("Vector indexes created")

    # Инициализация Kafka сервиса
    kafka_service = KafkaService()
    app.state.kafka_service = kafka_service
    print("Kafka service initialized")

    # Инициализация аналитики
    try:
        await analytics_service.initialize()
        print("Analytics service initialized")
    except Exception as e:
        print(f"Failed to initialize analytics: {e}")

    yield

    # Shutdown
    if hasattr(app.state, 'kafka_service'):
        app.state.kafka_service.close()
    print("Application shutdown complete")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API для приложения финансовой грамотности с поддержкой векторного поиска, AI и аналитики",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus middleware
prometheus_middleware = PrometheusMiddleware()
app.middleware("http")(prometheus_middleware)

# Подключение роутеров
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(lessons.router, prefix=settings.API_V1_STR)
app.include_router(gamification.router, prefix=settings.API_V1_STR)
app.include_router(ai_routes.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "message": "Financial Literacy App API",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "JWT Authentication",
            "Lesson Management",
            "Gamification System",
            "OpenAI Integration",
            "Vector Search",
            "Personalized Recommendations",
            "Kafka Event Processing",
            "Prometheus Metrics",
            "ClickHouse Analytics"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint для Kubernetes"""
    return {"status": "healthy"}


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint для Kubernetes"""
    return {"status": "ready"}


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(get_metrics(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
