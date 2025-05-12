from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
from app.api.clickhouse_client import ClickHouseClient
from app.api.config import Config

# Глобальный объект для управления ClickHouse клиентом
clickhouse_manager = None


def init_clickhouse(config):
    """Инициализация ClickHouse клиента."""
    global clickhouse_manager
    clickhouse_manager = ClickHouseClient(config)


def init_app(init_db=True):
    """
    Инициализация приложения stats.
    Запускает gRPC-сервер и Kafka-потребитель.
    """
    if init_db:
        init_clickhouse(Config)

    from app.api.stats import serve

    app = FastAPI(
        lifespan=serve,
        openapi_url="/api/v1/stats/openapi.json",
        docs_url="/api/v1/stats/docs"
    )
    return app
