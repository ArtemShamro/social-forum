#!/bin/sh

echo "Upgrading alembic"
cd app/app && alembic upgrade head && cd ../../

echo "Starting uvicorn"
uvicorn app:init_app --reload --host 0.0.0.0 --port 8000 --factory