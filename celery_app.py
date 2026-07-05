import os
from celery import Celery

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672//")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "heart_tasks",
    broker=RABBITMQ_URL,
    backend=REDIS_URL
)