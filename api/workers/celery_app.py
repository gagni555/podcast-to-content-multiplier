from celery import Celery
from config import settings

# Create Celery instance
celery_app = Celery('podcast_multiplier')

# Configure Celery
celery_app.conf.update(
    broker_url=settings.redis_url,
    result_backend=settings.redis_url,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Import tasks
from . import tasks

if __name__ == '__main__':
    celery_app.start()