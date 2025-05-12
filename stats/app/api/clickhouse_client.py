import os
import clickhouse_connect
import logging
import time
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ClickHouseClient:
    def __init__(self, config, retries=5, delay=2):
        logger.info(
            f"Инициализация ClickHouse клиента: host={config.CLICKHOUSE_HOST}, port={config.CLICKHOUSE_PORT}, database={config.CLICKHOUSE_DATABASE}")
        self.client = None
        for attempt in range(1, retries + 1):
            try:
                self.client = clickhouse_connect.get_client(
                    host=config.CLICKHOUSE_HOST,
                    port=config.CLICKHOUSE_PORT,
                    user=config.CLICKHOUSE_USER,
                    password=config.CLICKHOUSE_PASSWORD,
                    database=config.CLICKHOUSE_DATABASE,
                    interface='http'
                )
                logger.info("ClickHouse клиент успешно инициализирован")
                break
            except Exception as e:
                logger.warning(
                    f"Попытка {attempt}/{retries} подключения к ClickHouse не удалась: {e}")
                if attempt == retries:
                    logger.error(
                        f"Не удалось инициализировать ClickHouse клиент после {retries} попыток: {e}")
                    raise
                time.sleep(delay)
        self.init_schema()

    def init_schema(self):
        """Инициализация таблицы events."""
        schema_path = "/app/app/app/schema.sql"
        logger.info(f"Попытка загрузки схемы из {schema_path}")
        try:
            if not os.path.exists(schema_path):
                logger.error(f"Файл схемы {schema_path} не найден")
                raise FileNotFoundError(f"Файл схемы {schema_path} не найден")

            with open(schema_path, "r") as f:
                schema = f.read()
            logger.debug(f"Схема загружена: {schema}")

            self.client.command(schema)
            logger.info("Таблица events создана или уже существует")
        except Exception as e:
            logger.error(f"Ошибка инициализации схемы: {e}", exc_info=True)
            raise

    def validate_event(self, event: Dict) -> bool:
        """Валидация структуры события перед вставкой."""
        required_fields = {"event_type": str, "post_id": int,
                            "timestamp": datetime}
        optional_fields = {"user_id": str, "comment_id": (int, type(None))}

        for field, expected_type in required_fields.items():
            if field not in event:
                logger.error(
                    f"Отсутствует обязательное поле '{field}' в событии: {event}")
                return False
            if not isinstance(event[field], expected_type):
                logger.error(
                    f"Неверный тип для поля '{field}': ожидается {expected_type}, получено {type(event[field])}")
                return False

        for field, expected_types in optional_fields.items():
            if field in event and not isinstance(event[field], expected_types):
                logger.error(
                    f"Неверный тип для поля '{field}': ожидается {expected_types}, получено {type(event[field])}")
                return False

        return True

    def check_table_exists(self) -> bool:
        """Проверка существования таблицы stats_db.events."""
        try:
            result = self.client.query(
                "SELECT 1 FROM system.tables WHERE database = 'stats_db' AND name = 'events'")
            return bool(result.result_rows)
        except Exception as e:
            logger.error(
                f"Ошибка при проверке существования таблицы stats_db.events: {e}", exc_info=True)
            return False

    def insert_event(self, event: Dict):
        """Вставка одного события в таблицу events."""
        try:
            if not self.check_table_exists():
                logger.error("Таблица stats_db.events не существует")
                raise ValueError("Таблица stats_db.events не существует")

            if not self.validate_event(event):
                logger.error(f"Невалидное событие: {event}")
                raise ValueError(f"Невалидное событие: {event}")

            # Преобразуем словарь события в кортеж в порядке column_names
            event_tuple = (
                event["event_type"],
                event["post_id"],
                event["user_id"],
                event["comment_id"],
                event["timestamp"]
            )
            logger.debug(f"Подготовлено событие для вставки: {event_tuple}")

            self.client.insert(
                "stats_db.events",
                [event_tuple],
                column_names=["event_type", "post_id",
                              "user_id", "comment_id", "timestamp"]
            )
            logger.info(
                f"Записано событие: {event['event_type']} для post_id={event['post_id']}")
        except Exception as e:
            logger.error(
                f"Ошибка вставки события: {e}, событие: {event}", exc_info=True)
            raise

    def get_post_stats(self, post_id: int) -> Dict[str, int]:
        """Получение количества просмотров, лайков и комментариев для поста."""
        try:
            result = self.client.query(
                """
                SELECT
                    event_type,
                    count(*) as count
                FROM stats_db.events
                WHERE post_id = %s
                GROUP BY event_type
                """,
                parameters=(post_id,)
            )
            stats = {"views": 0, "likes": 0, "comments": 0}
            for row in result.result_rows:
                event_type, count = row
                if event_type == "view":
                    stats["views"] = count
                elif event_type == "like":
                    stats["likes"] = count
                elif event_type == "comment":
                    stats["comments"] = count
            return stats
        except Exception as e:
            logger.error(
                f"Ошибка получения статистики поста {post_id}: {e}", exc_info=True)
            return {"views": 0, "likes": 0, "comments": 0}

    def get_views_dynamics(self, post_id: int) -> List[Dict[str, any]]:
        """Получение динамики просмотров по дням для поста."""
        try:
            result = self.client.query(
                """
                SELECT
                    toDate(timestamp) as date,
                    count(*) as views
                FROM stats_db.events
                WHERE post_id = %s AND event_type = 'view'
                GROUP BY date
                ORDER BY date
                """,
                parameters=(post_id,)
            )
            return [{"date": str(row[0]), "views": row[1]} for row in result.result_rows]
        except Exception as e:
            logger.error(
                f"Ошибка получения динамики просмотров для поста {post_id}: {e}", exc_info=True)
            return []

    def get_likes_dynamics(self, post_id: int) -> List[Dict[str, any]]:
        """Получение динамики лайков по дням для поста."""
        try:
            result = self.client.query(
                """
                SELECT
                    toDate(timestamp) as date,
                    count(*) as likes
                FROM stats_db.events
                WHERE post_id = %s AND event_type = 'like'
                GROUP BY date
                ORDER BY date
                """,
                parameters=(post_id,)
            )
            return [{"date": str(row[0]), "likes": row[1]} for row in result.result_rows]
        except Exception as e:
            logger.error(
                f"Ошибка получения динамики лайков для поста {post_id}: {e}", exc_info=True)
            return []

    def get_comments_dynamics(self, post_id: int) -> List[Dict[str, any]]:
        """Получение динамики комментариев по дням для поста."""
        try:
            result = self.client.query(
                """
                SELECT
                    toDate(timestamp) as date,
                    count(*) as comments
                FROM stats_db.events
                WHERE post_id = %s AND event_type = 'comment'
                GROUP BY date
                ORDER BY date
                """,
                parameters=(post_id,)
            )
            return [{"date": str(row[0]), "comments": row[1]} for row in result.result_rows]
        except Exception as e:
            logger.error(
                f"Ошибка получения динамики комментариев для поста {post_id}: {e}", exc_info=True)
            return []

    def get_top_posts(self, metric: str) -> List[Dict[str, any]]:
        """Получение топ-10 постов по количеству лайков, комментариев или просмотров."""
        if metric not in ["like", "view", "comment"]:
            raise ValueError("metric должен быть 'like', 'view' или 'comment'")
        try:
            result = self.client.query(
                """
                SELECT
                    post_id,
                    count(*) as count
                FROM stats_db.events
                WHERE event_type = %s
                GROUP BY post_id
                ORDER BY count DESC
                LIMIT 10
                """,
                parameters=(metric,)
            )
            print("result.result_rows", result.result_rows)
            return [{"post_id": row[0], "count": row[1]} for row in result.result_rows]
        except Exception as e:
            logger.error(
                f"Ошибка получения топ-10 постов по {metric}: {e}", exc_info=True)
            return []

    def get_top_users(self, metric: str) -> List[Dict[str, any]]:
        """Получение топ-10 пользователей по количеству лайков, комментариев или просмотров."""
        if metric not in ["like", "post", "comment"]:
            raise ValueError("metric должен быть 'like', 'post' или 'comment'")
        try:
            result = self.client.query(
                """
                SELECT
                    user_id,
                    count(*) as count
                FROM stats_db.events
                WHERE event_type = %s
                GROUP BY user_id
                ORDER BY count DESC
                LIMIT 10
                """,
                parameters=(metric,)
            )
            print("result.result_rows", result.result_rows)
            return [{"user_id": row[0], "count": row[1]} for row in result.result_rows]
        except Exception as e:
            logger.error(
                f"Ошибка получения топ-10 пользователей по {metric}: {e}", exc_info=True)
            return []

    def get_post_stats(self, post_id: int) -> Dict[str, int]:
        """Получение количества просмотров, лайков и комментариев для поста."""
        try:
            result = self.client.query(
                """
                SELECT event_type, post_id, count(*) value from stats_db.events e2 
                WHERE post_id = %s
                GROUP BY event_type, post_id 
                """,
                parameters=(post_id,)
            )
            logger.info("result.result_rows %s", result.result_rows)
            # Initialize all stats to 0
            stats = {"view": 0, "comment": 0, "like": 0}
            for row in result.result_rows:
                event_type, _, value = row
                if event_type in stats:
                    stats[event_type] = value
            return stats
        except Exception as e:
            logger.error(
                f"Ошибка получения статистики поста {post_id}: {e}", exc_info=True)
            return {"view": 0, "comment": 0, "like": 0}
    
    def disconnect(self):
        """Закрытие соединения с ClickHouse."""
        if self.client:
            self.client.close()
