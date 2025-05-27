from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import redis
from config import settings
import logging

logger = logging.getLogger(__name__)

# PostgreSQL Database с поддержкой pgvector
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Redis connection
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_db():
    """Dependency для получения сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    """Dependency для получения Redis клиента"""
    return redis_client


async def init_db():
    """Инициализация базы данных с поддержкой pgvector"""
    try:
        # Создаем расширение pgvector если его нет
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            logger.info("pgvector extension enabled")

        # Создаем таблицы
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def create_vector_index():
    """Создание индексов для векторного поиска"""
    try:
        with engine.connect() as conn:
            # Создаем HNSW индекс для быстрого поиска по векторам
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS lesson_content_embedding_idx 
                ON lesson_embeddings USING hnsw (embedding vector_cosine_ops)
            """))

            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS knowledge_base_embedding_idx 
                ON knowledge_base USING hnsw (embedding vector_cosine_ops)
            """))

            conn.commit()
            logger.info("Vector indexes created successfully")

    except Exception as e:
        logger.error(f"Error creating vector indexes: {e}")
        raise
