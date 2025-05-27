import json
import logging
from typing import Dict, Any, Optional
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from config import settings
import asyncio
from datetime import datetime


class KafkaService:
    def __init__(self):
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.producer = None
        self.consumers = {}
        self.logger = logging.getLogger(__name__)

    def get_producer(self) -> KafkaProducer:
        """Получение Kafka producer"""
        if not self.producer:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(
                    v, default=str).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                retries=3,
                retry_backoff_ms=1000
            )
        return self.producer

    def get_consumer(self, topic: str, group_id: str) -> KafkaConsumer:
        """Получение Kafka consumer"""
        consumer_key = f"{topic}_{group_id}"

        if consumer_key not in self.consumers:
            self.consumers[consumer_key] = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                auto_offset_reset='latest',
                enable_auto_commit=True
            )

        return self.consumers[consumer_key]

    async def publish_user_event(self, user_id: int, event_type: str, data: Dict[str, Any]):
        """Публикация события пользователя"""
        event = {
            "user_id": user_id,
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "financial_literacy_app"
        }

        await self._publish_event(settings.KAFKA_TOPIC_USER_EVENTS, str(user_id), event)

    async def publish_lesson_event(self, user_id: int, lesson_id: int, event_type: str, data: Dict[str, Any]):
        """Публикация события урока"""
        event = {
            "user_id": user_id,
            "lesson_id": lesson_id,
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "financial_literacy_app"
        }

        await self._publish_event(settings.KAFKA_TOPIC_LESSON_EVENTS, f"{user_id}_{lesson_id}", event)

    async def publish_gamification_event(self, user_id: int, event_type: str, data: Dict[str, Any]):
        """Публикация события геймификации"""
        event = {
            "user_id": user_id,
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "financial_literacy_app"
        }

        await self._publish_event(settings.KAFKA_TOPIC_GAMIFICATION, str(user_id), event)

    async def _publish_event(self, topic: str, key: str, event: Dict[str, Any]):
        """Базовый метод для публикации события"""
        try:
            producer = self.get_producer()
            future = producer.send(topic, key=key, value=event)

            # Ждем подтверждения отправки
            record_metadata = future.get(timeout=10)

            self.logger.info(
                f"Event published to topic {topic}, partition {record_metadata.partition}, "
                f"offset {record_metadata.offset}"
            )

        except KafkaError as e:
            self.logger.error(f"Failed to publish event to topic {topic}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error publishing event: {e}")
            raise

    async def consume_user_events(self, group_id: str = "user_events_processor"):
        """Потребление событий пользователей"""
        consumer = self.get_consumer(
            settings.KAFKA_TOPIC_USER_EVENTS, group_id)

        try:
            for message in consumer:
                await self._process_user_event(message.value)
        except Exception as e:
            self.logger.error(f"Error consuming user events: {e}")
        finally:
            consumer.close()

    async def consume_lesson_events(self, group_id: str = "lesson_events_processor"):
        """Потребление событий уроков"""
        consumer = self.get_consumer(
            settings.KAFKA_TOPIC_LESSON_EVENTS, group_id)

        try:
            for message in consumer:
                await self._process_lesson_event(message.value)
        except Exception as e:
            self.logger.error(f"Error consuming lesson events: {e}")
        finally:
            consumer.close()

    async def consume_gamification_events(self, group_id: str = "gamification_processor"):
        """Потребление событий геймификации"""
        consumer = self.get_consumer(
            settings.KAFKA_TOPIC_GAMIFICATION, group_id)

        try:
            for message in consumer:
                await self._process_gamification_event(message.value)
        except Exception as e:
            self.logger.error(f"Error consuming gamification events: {e}")
        finally:
            consumer.close()

    async def _process_user_event(self, event: Dict[str, Any]):
        """Обработка события пользователя"""
        event_type = event.get("event_type")
        user_id = event.get("user_id")

        self.logger.info(
            f"Processing user event: {event_type} for user {user_id}")

        # Здесь была бы логика обработки различных типов событий
        if event_type == "user_registered":
            await self._handle_user_registration(event)
        elif event_type == "user_login":
            await self._handle_user_login(event)
        elif event_type == "profile_updated":
            await self._handle_profile_update(event)

    async def _process_lesson_event(self, event: Dict[str, Any]):
        """Обработка события урока"""
        event_type = event.get("event_type")
        user_id = event.get("user_id")
        lesson_id = event.get("lesson_id")

        self.logger.info(
            f"Processing lesson event: {event_type} for user {user_id}, lesson {lesson_id}")

        if event_type == "lesson_started":
            await self._handle_lesson_started(event)
        elif event_type == "lesson_completed":
            await self._handle_lesson_completed(event)
        elif event_type == "quiz_answered":
            await self._handle_quiz_answered(event)

    async def _process_gamification_event(self, event: Dict[str, Any]):
        """Обработка события геймификации"""
        event_type = event.get("event_type")
        user_id = event.get("user_id")

        self.logger.info(
            f"Processing gamification event: {event_type} for user {user_id}")

        if event_type == "coins_earned":
            await self._handle_coins_earned(event)
        elif event_type == "challenge_completed":
            await self._handle_challenge_completed(event)
        elif event_type == "achievement_unlocked":
            await self._handle_achievement_unlocked(event)

    # Обработчики конкретных событий
    async def _handle_user_registration(self, event: Dict[str, Any]):
        """Обработка регистрации пользователя"""
        # Отправка приветственного email, создание начальных данных и т.д.
        pass

    async def _handle_user_login(self, event: Dict[str, Any]):
        """Обработка входа пользователя"""
        # Обновление статистики, проверка ежедневных бонусов и т.д.
        pass

    async def _handle_profile_update(self, event: Dict[str, Any]):
        """Обработка обновления профиля"""
        # Пересчет персонального плана, обновление рекомендаций и т.д.
        pass

    async def _handle_lesson_started(self, event: Dict[str, Any]):
        """Обработка начала урока"""
        # Логирование прогресса, обновление статистики и т.д.
        pass

    async def _handle_lesson_completed(self, event: Dict[str, Any]):
        """Обработка завершения урока"""
        # Начисление коинов, проверка достижений, обновление прогресса и т.д.
        pass

    async def _handle_quiz_answered(self, event: Dict[str, Any]):
        """Обработка ответа на тест"""
        # Валидация ответа, начисление очков, обновление статистики и т.д.
        pass

    async def _handle_coins_earned(self, event: Dict[str, Any]):
        """Обработка начисления коинов"""
        # Обновление баланса, проверка достижений и т.д.
        pass

    async def _handle_challenge_completed(self, event: Dict[str, Any]):
        """Обработка завершения челленджа"""
        # Начисление наград, обновление рейтинга и т.д.
        pass

    async def _handle_achievement_unlocked(self, event: Dict[str, Any]):
        """Обработка разблокировки достижения"""
        # Отправка уведомлений, обновление профиля и т.д.
        pass

    def close(self):
        """Закрытие соединений"""
        if self.producer:
            self.producer.close()

        for consumer in self.consumers.values():
            consumer.close()

        self.consumers.clear()
