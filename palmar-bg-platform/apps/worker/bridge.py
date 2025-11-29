"""
BullMQ to Celery Bridge
Listens to BullMQ jobs from Node.js API and triggers Celery tasks
"""
import redis
import json
import time
from app.tasks import celery_app, process_image_task
from app.core.config import settings

# Connect to Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=settings.REDIS_DB,
    decode_responses=True
)


def map_bullmq_to_celery(bullmq_data: dict) -> dict:
    """
    Map BullMQ job data to Celery task parameters

    BullMQ data structure:
    {
        "imageId": str,
        "userId": str,
        "s3Key": str,
        "backgroundType": str,
        "backgroundConfig": {...},
        "downloadTier": str
    }

    Celery task parameters:
    {
        "image_id": str,
        "user_id": str,
        "s3_original_key": str,
        "background_options": {...}
    }
    """
    background_type = bullmq_data.get('backgroundType', 'TRANSPARENT')
    background_config = bullmq_data.get('backgroundConfig', {})

    # Map background options
    background_options = None
    if background_type != 'TRANSPARENT':
        if background_type == 'SOLID':
            background_options = {
                'type': 'solid',
                'color': background_config.get('color', '#FFFFFF')
            }
        elif background_type == 'GRADIENT':
            # Parse gradient colors (assuming format like "#FF0000,#00FF00")
            color_str = background_config.get('color', '#FFFFFF,#000000')
            colors = color_str.split(',') if ',' in color_str else ['#FFFFFF', '#000000']
            background_options = {
                'type': 'gradient',
                'colors': colors,
                'angle': background_config.get('angle', 0)
            }
        elif background_type == 'TEXTURE':
            background_options = {
                'type': 'texture',
                'texture': background_config.get('textureType', 'wood')
            }

    return {
        'image_id': bullmq_data['imageId'],
        'user_id': bullmq_data['userId'],
        's3_original_key': bullmq_data['s3Key'],
        'background_options': background_options
    }


def process_bullmq_job(job_data_str: str, job_id: str):
    """
    Process a BullMQ job by triggering Celery task

    Args:
        job_data_str: JSON string of job data
        job_id: BullMQ job ID
    """
    try:
        # Parse job data
        job_data = json.loads(job_data_str)
        print(f"📨 Received BullMQ job {job_id}: {job_data.get('imageId')}")

        # Map to Celery parameters
        celery_params = map_bullmq_to_celery(job_data)

        # Trigger Celery task
        result = process_image_task.apply_async(
            kwargs=celery_params,
            task_id=job_id  # Use same ID for traceability
        )

        print(f"✓ Triggered Celery task {result.id} for image {celery_params['image_id']}")

        return True

    except Exception as e:
        print(f"✗ Failed to process BullMQ job {job_id}: {e}")
        import traceback
        traceback.print_exc()
        return False


def listen_to_bullmq_queue(queue_name: str = 'image-processing'):
    """
    Listen to BullMQ queue and process jobs

    Args:
        queue_name: Name of the BullMQ queue to listen to
    """
    print(f"🎧 Bridge listening to BullMQ queue: {queue_name}")
    print(f"   Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")

    # BullMQ stores jobs in Redis with specific key patterns
    # Pattern: bull:{queue_name}:waiting
    waiting_key = f"bull:{queue_name}:wait"
    active_key = f"bull:{queue_name}:active"
    completed_key = f"bull:{queue_name}:completed"

    while True:
        try:
            # Use BRPOPLPUSH to atomically move job from waiting to active
            # This ensures reliability - if we crash, job stays in active list
            result = redis_client.brpoplpush(waiting_key, active_key, timeout=5)

            if result:
                # Get job ID
                job_id = result

                # Get job data from Redis hash
                job_data_key = f"bull:{queue_name}:{job_id}"
                job_data_str = redis_client.hget(job_data_key, 'data')

                if job_data_str:
                    # Process the job
                    success = process_bullmq_job(job_data_str, job_id)

                    if success:
                        # Move from active to completed
                        redis_client.lrem(active_key, 1, job_id)
                        redis_client.lpush(completed_key, job_id)
                        print(f"✓ Job {job_id} marked as completed")
                    else:
                        # Keep in active for retry or manual intervention
                        print(f"⚠️  Job {job_id} failed, keeping in active queue")

                else:
                    print(f"⚠️  Job {job_id} data not found in Redis")
                    redis_client.lrem(active_key, 1, job_id)

            else:
                # No jobs available, continue listening
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n🛑 Bridge shutting down...")
            break

        except Exception as e:
            print(f"✗ Bridge error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(5)  # Wait before retrying


if __name__ == "__main__":
    print("=" * 60)
    print("  Palmar BG - BullMQ to Celery Bridge")
    print("=" * 60)
    print(f"  Version: 1.0.0")
    print(f"  Environment: {settings.DEBUG and 'Development' or 'Production'}")
    print("=" * 60)

    try:
        # Test Redis connection
        redis_client.ping()
        print("✓ Connected to Redis")

        # Start listening
        listen_to_bullmq_queue()

    except Exception as e:
        print(f"✗ Bridge startup failed: {e}")
        import traceback
        traceback.print_exc()
