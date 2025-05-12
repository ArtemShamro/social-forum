import json
import logging
import asyncio
from aiokafka import AIOKafkaConsumer
from dateutil.parser import isoparse
from app.api.clickhouse_client import ClickHouseClient

logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(self, clickhouse_manager: ClickHouseClient):
        self.consumer = AIOKafkaConsumer(
            "post_like", "post_view", "post_comment", "user_registration", "post_create",
            bootstrap_servers="kafka:9092",
            group_id="stats_group",
            auto_offset_reset="earliest",
            max_poll_interval_ms=60000,
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000
        )
        self.clickhouse_manager = clickhouse_manager

    async def start(self):
        """Запуск Kafka-потребителя с обработкой ошибок подключения."""
        logger.info("Запуск Kafka-потребителя")
        retries = 5
        for attempt in range(1, retries + 1):
            try:
                await self.consumer.start()
                logger.info("Kafka-потребитель успешно запущен")
                return
            except Exception as e:
                logger.error(
                    f"Попытка {attempt}/{retries} подключения к Kafka не удалась: {e}")
                if attempt == retries:
                    logger.error(
                        f"Не удалось запустить Kafka-потребитель после {retries} попыток")
                    raise
                await asyncio.sleep(2)

    async def stop(self):
        """Остановка Kafka-потребителя."""
        logger.info("Остановка Kafka-потребителя")
        try:
            await self.consumer.stop()
            logger.info("Kafka-потребитель успешно остановлен")
        except Exception as e:
            logger.error(f"Ошибка при остановке Kafka-потребителя: {e}")

    async def consume(self):
        """Чтение и обработка сообщений из Kafka."""
        logger.info("Начало обработки сообщений из Kafka")
        try:
            async for msg in self.consumer:
                await self.process_message(msg)
        except Exception as e:
            logger.error(
                f"Ошибка в цикле обработки сообщений: {e}", exc_info=True)
            raise
        finally:
            await self.stop()

    async def process_message(self, msg):
        """Обработка одного сообщения."""
        try:
            topic = msg.topic
            message = json.loads(msg.value.decode("utf-8"))
            logger.info(f"Получено сообщение из топика {topic}: {message}")

            # Определяем тип события на основе топика
            if topic == "user_registration":
                event_type = "registration"
                comment_id = None
            elif topic == "post_like":
                event_type = "like"
                comment_id = None
            elif topic == "post_view":
                event_type = "view"
                comment_id = None
            elif topic == "post_create":
                event_type = "post"
                comment_id = None
            elif topic == "post_comment":
                event_type = "comment"
                comment_id = message.get("comment_id")
            else:
                logger.warning(f"Неизвестный топик: {topic}")
                return

            # Парсинг времени с помощью dateutil.parser
            timestamp_str = message.get("timestamp")
            if not timestamp_str:
                logger.error(
                    f"Поле timestamp отсутствует в сообщении: {message}")
                return
            try:
                timestamp = isoparse(timestamp_str)
            except ValueError as e:
                logger.error(
                    f"Ошибка парсинга timestamp '{timestamp_str}' в сообщении: {message}. Ошибка: {e}")
                return

            # Формируем данные для вставки
            event = {
                "event_type": event_type,
                "post_id": message.get("post_id", 0),
                "user_id": message.get("user_id", ""),
                "comment_id": comment_id,
                "timestamp": timestamp
            }
            logger.debug(f"Сформировано событие для вставки: {event}")

            # Вставка в ClickHouse
            self.clickhouse_manager.insert_event(event)
            logger.info(
                f"Обработано сообщение из топика {topic} для post_id={event['post_id']}")
        except json.JSONDecodeError as e:
            logger.error(
                f"Ошибка декодирования JSON в сообщении из топика {topic}: {e}", exc_info=True)
        except Exception as e:
            logger.error(
                f"Ошибка обработки сообщения из топика {topic}: {e}, сообщение: {message}", exc_info=True)
