"""
Main image processing Celery task
Orchestrates background removal, optimization, and S3 upload
"""
from celery import Task
from app.tasks.celery_app import celery_app
from app.services import BackgroundRemovalService, ImageOptimizationService, BackgroundEditorService
from app.core.s3 import s3_client
from app.core.database import AsyncSessionLocal
from sqlalchemy import text
from typing import Dict, Any, Optional
import asyncio


class CallbackTask(Task):
    """Base task with callbacks for lifecycle events"""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure"""
        print(f'Task {task_id} failed: {exc}')

    def on_success(self, retval, task_id, args, kwargs):
        """Handle task success"""
        print(f'Task {task_id} succeeded')


@celery_app.task(
    base=CallbackTask,
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name='app.tasks.process_image.process_image_task'
)
def process_image_task(
    self,
    image_id: str,
    user_id: str,
    s3_original_key: str,
    background_options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process image with background removal and customization

    Args:
        image_id: Database image ID
        user_id: User ID who owns the image
        s3_original_key: S3 key for original image
        background_options: Optional background customization
            {
                "type": "solid" | "gradient" | "texture",
                "color": "#FFFFFF",  # For solid
                "colors": ["#FF0000", "#00FF00"],  # For gradient
                "angle": 45,  # For gradient
                "texture": "wood"  # For texture
            }

    Returns:
        Dict with processing results
    """
    try:
        print(f"Processing image {image_id} for user {user_id}")

        # Update status to PROCESSING
        asyncio.run(_update_image_status(image_id, 'PROCESSING'))

        # Step 1: Download original image from S3
        print(f"Downloading from S3: {s3_original_key}")
        original_image_bytes = s3_client.download_file(s3_original_key)

        if not original_image_bytes:
            raise Exception("Failed to download original image from S3")

        # Step 2: Remove background
        print("Removing background...")
        bg_service = BackgroundRemovalService()
        transparent_image_bytes = bg_service.remove_background(original_image_bytes)

        if not transparent_image_bytes:
            raise Exception("Background removal failed")

        # Step 3: Apply background customization if requested
        if background_options:
            print(f"Applying background: {background_options}")
            editor_service = BackgroundEditorService()

            bg_type = background_options.get('type', 'transparent')

            if bg_type == 'solid':
                color = background_options.get('color', '#FFFFFF')
                transparent_image_bytes = editor_service.add_solid_background(
                    transparent_image_bytes,
                    color
                )

            elif bg_type == 'gradient':
                colors = background_options.get('colors', ['#FFFFFF', '#000000'])
                angle = background_options.get('angle', 0)
                transparent_image_bytes = editor_service.add_gradient_background(
                    transparent_image_bytes,
                    colors,
                    angle
                )

            elif bg_type == 'texture':
                texture = background_options.get('texture', 'wood')
                transparent_image_bytes = editor_service.add_texture_background(
                    transparent_image_bytes,
                    texture
                )

        # Step 4: Generate multi-resolution outputs
        print("Generating multi-resolution outputs...")
        optimizer = ImageOptimizationService()
        resolutions = optimizer.generate_multi_resolution(transparent_image_bytes)

        if not resolutions:
            raise Exception("Multi-resolution generation failed")

        # Step 5: Upload all versions to S3
        print("Uploading processed images to S3...")
        s3_keys = {}

        # Upload small version (always available)
        small_key = f"processed/{user_id}/{image_id}/small.png"
        if s3_client.upload_file(resolutions['small'], small_key, 'image/png'):
            s3_keys['small'] = small_key

        # Upload HD version
        hd_key = f"processed/{user_id}/{image_id}/hd.png"
        if s3_client.upload_file(resolutions['hd'], hd_key, 'image/png'):
            s3_keys['hd'] = hd_key

        # Upload Ultra HD version
        ultra_hd_key = f"processed/{user_id}/{image_id}/ultra_hd.png"
        if s3_client.upload_file(resolutions['ultra_hd'], ultra_hd_key, 'image/png'):
            s3_keys['ultra_hd'] = ultra_hd_key

        # Step 6: Update database with S3 keys and status
        print("Updating database...")
        asyncio.run(_update_image_results(
            image_id,
            s3_keys.get('small'),
            s3_keys.get('hd'),
            s3_keys.get('ultra_hd')
        ))

        print(f"✓ Successfully processed image {image_id}")

        return {
            'success': True,
            'image_id': image_id,
            's3_keys': s3_keys,
            'message': 'Image processed successfully'
        }

    except Exception as exc:
        print(f"✗ Processing failed for image {image_id}: {exc}")

        # Update status to FAILED
        try:
            asyncio.run(_update_image_status(image_id, 'FAILED', str(exc)))
        except:
            pass

        # Retry logic
        if self.request.retries < self.max_retries:
            print(f"Retrying... (attempt {self.request.retries + 1}/{self.max_retries})")
            raise self.retry(exc=exc)

        return {
            'success': False,
            'image_id': image_id,
            'error': str(exc)
        }


async def _update_image_status(
    image_id: str,
    status: str,
    error_message: Optional[str] = None
):
    """Update image processing status in database"""
    try:
        async with AsyncSessionLocal() as session:
            if error_message:
                query = text("""
                    UPDATE "Image"
                    SET status = :status, "errorMessage" = :error_message, "updatedAt" = NOW()
                    WHERE id = :image_id
                """)
                await session.execute(
                    query,
                    {"status": status, "error_message": error_message, "image_id": image_id}
                )
            else:
                query = text("""
                    UPDATE "Image"
                    SET status = :status, "updatedAt" = NOW()
                    WHERE id = :image_id
                """)
                await session.execute(query, {"status": status, "image_id": image_id})

            await session.commit()
            print(f"✓ Updated image {image_id} status to {status}")

    except Exception as e:
        print(f"✗ Failed to update image status: {e}")


async def _update_image_results(
    image_id: str,
    small_url: Optional[str],
    hd_url: Optional[str],
    ultra_hd_url: Optional[str]
):
    """Update image with processed S3 URLs"""
    try:
        async with AsyncSessionLocal() as session:
            query = text("""
                UPDATE "Image"
                SET
                    status = 'COMPLETED',
                    "processedSmallUrl" = :small_url,
                    "processedHdUrl" = :hd_url,
                    "processedUltraHdUrl" = :ultra_hd_url,
                    "processedAt" = NOW(),
                    "updatedAt" = NOW()
                WHERE id = :image_id
            """)

            await session.execute(query, {
                "image_id": image_id,
                "small_url": small_url,
                "hd_url": hd_url,
                "ultra_hd_url": ultra_hd_url
            })

            await session.commit()
            print(f"✓ Updated image {image_id} with processed URLs")

    except Exception as e:
        print(f"✗ Failed to update image results: {e}")
        raise
