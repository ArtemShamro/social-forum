#!/bin/bash
set -e

# Проверка наличия nc
if ! command -v nc >/dev/null 2>&1; then
    echo "Ошибка: netcat (nc) не установлен в контейнере"
    exit 1
fi

# Ожидание доступности ClickHouse
echo "Ожидание готовности ClickHouse на clickhouse:8123..."
attempt=1
max_attempts=30
until nc -z clickhouse 8123; do
    echo "Попытка $attempt/$max_attempts: ClickHouse недоступен - ждём..."
    sleep 1
    ((attempt++))
    if [ $attempt -gt $max_attempts ]; then
        echo "Ошибка: ClickHouse не стал доступен после $max_attempts попыток"
        exit 1
    fi
done
echo "ClickHouse готов и принимает соединения"

# Ожидание доступности Kafka
echo "Ожидание готовности Kafka на kafka:9092..."
attempt=1
max_attempts=30
until nc -z kafka 9092; do
    echo "Попытка $attempt/$max_attempts: Kafka недоступен - ждём..."
    sleep 1
    ((attempt++))
    if [ $attempt -gt $max_attempts ]; then
        echo "Ошибка: Kafka не стал доступен после $max_attempts попыток"
        exit 1
    fi
done
echo "Kafka готов и принимает соединения"

# Запуск приложения
exec uvicorn app:init_app --reload --host 0.0.0.0 --port 8000 --factory