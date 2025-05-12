import logging
import sys
import grpc
from concurrent import futures
from contextlib import asynccontextmanager
from proto import stats_pb2
from proto import stats_pb2_grpc
from app import clickhouse_manager
from app.api.kafka_consumer import KafkaConsumer
import asyncio

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Изменено на INFO для отладки
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Фильтр для исключения избыточных сообщений


class KafkaLogFilter(logging.Filter):
    def filter(self, record):
        # Исключаем сообщения от aiokafka с уровнем DEBUG
        if record.name.startswith("aiokafka") and record.levelno <= logging.INFO:
            return False
        return True


logger.addFilter(KafkaLogFilter())


class StatsServicer(stats_pb2_grpc.StatsServiceServicer):
    async def GetCount(self, request, context):
        logger.info(f"Received GetCount request: {request}")
        target_type = request.targetType
        if target_type not in ["like", "view", "comment"]:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Invalid targetType: {target_type}")

        stats = await clickhouse_manager.get_post_stats(request.post_id)
        count = stats.get(f"{target_type}s", 0)  # views, likes, comments
        return stats_pb2.GetCountResponse(counter=count)

    async def GetDynamics(self, request, context):
        logger.info(f"Received GetDynamics request: {request}")
        target_type = request.targetType
        if target_type not in ["like", "view", "comment"]:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Invalid targetType: {target_type}")

        if target_type == "view":
            dynamics = await clickhouse_manager.get_views_dynamics(request.post_id)
        elif target_type == "like":
            dynamics = await clickhouse_manager.get_likes_dynamics(request.post_id)
        else:  # comment
            dynamics = await clickhouse_manager.get_comments_dynamics(request.post_id)

        day_data = [
            stats_pb2.DayData(date=item["date"], value=item[f"{target_type}s"])
            for item in dynamics
        ]
        return stats_pb2.GetDynamicsResponse(dayData=day_data)

    async def GetTopPosts(self, request, context):
        logger.info(f"Received GetTopPosts request: {request}")
        target_type = request.targetType
        limit = request.limit or 10  # По умолчанию 10
        if target_type not in ["like", "view", "comment"]:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Invalid targetType: {target_type}")

        top_posts = clickhouse_manager.get_top_posts(target_type)
        print("top_posts", top_posts)
        posts_data = [
            stats_pb2.TopStatsResponse(id=int(item["post_id"]), value=int(item["count"]))
            for item in top_posts[:limit]
        ]
        return stats_pb2.GetTopResponse(items=posts_data)

    async def GetTopUsers(self, request, context):
        logger.info(f"Received GetTopUsers request: {request}")
        target_type = request.targetType
        limit = request.limit or 10  # По умолчанию 10
        if target_type not in ["like", "post", "comment"]:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Invalid targetType: {target_type}")

        top_users = clickhouse_manager.get_top_users(target_type)
        logger.info(f"Stats: top users: {top_users}")

        users_data = [
            stats_pb2.TopStatsResponse(id=int(item["user_id"]), value=int(item["count"]))
            for item in top_users[:limit]
        ]

        return stats_pb2.GetTopResponse(items=users_data)
    
    async def GetPostStats(self, request, context):
        logger.info(f"Received GetPostStats request: {request}")
        post_id = request.post_id
        stats = clickhouse_manager.get_post_stats(post_id)
        return stats_pb2.GetPostStatsResponse(views=stats["view"], likes=stats["like"], comments=stats["comment"])


@asynccontextmanager
async def serve(app):
    logger.info("Starting gRPC server and Kafka consumer...")

    # Инициализация Kafka
    kafka_consumer = KafkaConsumer(clickhouse_manager)
    await kafka_consumer.start()

    # Запуск gRPC-сервера
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    stats_pb2_grpc.add_StatsServiceServicer_to_server(StatsServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()

    # Запуск Kafka-потребителя в фоновом режиме
    kafka_task = asyncio.create_task(kafka_consumer.consume())

    try:
        yield
    finally:
        logger.info("Shutting down gRPC server and Kafka consumer...")
        kafka_task.cancel()
        await kafka_consumer.stop()
        clickhouse_manager.disconnect()
        await server.stop(grace=2)
