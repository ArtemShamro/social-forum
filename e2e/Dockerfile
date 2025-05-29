FROM python:3.11-slim

WORKDIR /app
COPY ./e2e/requirements.txt .
RUN pip install -r requirements.txt

COPY e2e/tests/ /app/tests/
COPY e2e/scripts/wait-for-services.sh /app/
RUN chmod +x /app/wait-for-services.sh

CMD ["./wait-for-services.sh", "proxy:8000", "auth:8000", "kafka:9092", "--", "pytest", "/app/tests/"]
