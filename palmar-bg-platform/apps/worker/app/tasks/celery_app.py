"""
Celery application configuration
"""
from celery import Celery
from celery.signals import worker_process_init
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "palmar_bg_worker",
    broker=settings.celery_broker,
    backend=settings.celery_backend,
    include=['app.tasks.process_image']
)


@worker_process_init.connect
def init_worker(**kwargs):
    """
    Initialize connections when Celery worker process starts
    This runs in each forked worker process
    """
    from app.core.s3 import s3_client

    print("🔧 Initializing Celery worker process...")

    # Initialize S3 client in this worker process
    try:
        s3_client.connect()
        print(f"✓ S3 connected in worker process: {s3_client.bucket_name}")
    except Exception as e:
        print(f"✗ Failed to connect S3 in worker: {e}")

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.TASK_TIME_LIMIT,
    task_soft_time_limit=settings.TASK_SOFT_TIME_LIMIT,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    broker_connection_retry_on_startup=True,
)

# Task routes
celery_app.conf.task_routes = {
    'app.tasks.process_image.process_image_task': {
        'queue': 'image_processing'
    }
}

if __name__ == '__main__':
    celery_app.start()
