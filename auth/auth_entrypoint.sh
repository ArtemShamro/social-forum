#!/bin/sh

cd app && alembic upgrade head && cd ../

uvicorn app:init_app --reload --host 0.0.0.0 --port 8000 --factory