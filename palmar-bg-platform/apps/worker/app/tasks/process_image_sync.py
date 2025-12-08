"""
Synchronous image processing function
All I/O operations are synchronous (boto3, rembg, PIL)
This is called from FastAPI via ThreadPoolExecutor
"""
import time
import logging
from app.services import BackgroundRemovalService
from app.core.s3 import s3_client
from app.core.database import update_image_in_database
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def process_image_sync(
    image_id: str,
    user_id: str,
    s3_original_key: str,
    background_options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process image with background removal (SYNCHRONOUS)

    Complete pipeline:
    1. Download original from S3
    2. Remove background using AI model
    3. Upload processed image to S3
    4. Update database DIRECTLY (bypasses API auth)

    This function is designed to run in Celery workers
    All I/O operations are synchronous (boto3, rembg, PIL)
    """
    start_time = time.time()

    try:
        logger.info(f"🚀 Starting image processing pipeline")
        logger.info(f"   Image ID: {image_id}")
        logger.info(f"   User ID: {user_id}")
        logger.info(f"   S3 Key: {s3_original_key}")

        # Update status to PROCESSING
        update_image_in_database(image_id, {
            'processing_status': 'PROCESSING'
        })

        # Step 1: Download original image from S3
        logger.info(f"📥 Step 1/4: Downloading original image from S3...")
        original_image_bytes = s3_client.download_file(s3_original_key)

        if not original_image_bytes:
            raise Exception("Failed to download original image from S3")

        logger.info(f"   Downloaded {len(original_image_bytes)} bytes")

        # Step 2: Remove background
        logger.info(f"🎨 Step 2/4: Processing image with AI model...")
        bg_service = BackgroundRemovalService()
        transparent_image_bytes = bg_service.remove_background(original_image_bytes)

        if not transparent_image_bytes:
            raise Exception("Background removal failed")

        logger.info(f"   Processed {len(transparent_image_bytes)} bytes")

        # Step 3: Upload processed image to S3
        # Generate processed key from original key
        # e.g., "images/user-id/timestamp_filename.jpg" -> "images/user-id/processed_timestamp_filename.png"
        path_parts = s3_original_key.rsplit('/', 1)
        if len(path_parts) == 2:
            filename = path_parts[1]
            # Remove extension and add .png
            filename_no_ext = filename.rsplit('.', 1)[0]
            processed_key = f"{path_parts[0]}/processed_{filename_no_ext}.png"
        else:
            processed_key = f"processed_{s3_original_key}.png"

        logger.info(f"📤 Step 3/4: Uploading processed image to S3...")
        logger.info(f"   Processed S3 key: {processed_key}")

        upload_success = s3_client.upload_file(
            transparent_image_bytes,
            processed_key,
            content_type="image/png"
        )

        if not upload_success:
            raise Exception("Failed to upload processed image to S3")

        logger.info(f"   Uploaded successfully")

        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)

        # Step 4: Update database DIRECTLY (no API authentication needed)
        # CRITICAL: Update both processed_s3_key (legacy) and processed_small_url (used by API)
        # The API service looks for processedSmallUrl to generate presigned URLs
        logger.info(f"💾 Step 4/4: Updating database with results...")
        success = update_image_in_database(image_id, {
            'processed_s3_key': processed_key,  # Legacy field (for reference)
            'processed_small_url': processed_key,  # API looks for this field!
            'processing_status': 'COMPLETED',
            'processing_time_ms': processing_time,
            'processed_file_size': len(transparent_image_bytes)
        })

        if not success:
            raise Exception("Failed to update database with processing results")

        logger.info(f"✅ Image processing completed successfully!")
        logger.info(f"   Processing time: {processing_time}ms")
        logger.info(f"   Processed size: {len(transparent_image_bytes)} bytes")

        return {
            'success': True,
            'image_id': image_id,
            'processed_s3_key': processed_key,
            'processing_time_ms': processing_time,
            'processed_file_size': len(transparent_image_bytes),
            'original_file_size': len(original_image_bytes)
        }

    except Exception as exc:
        processing_time = int((time.time() - start_time) * 1000)
        error_message = str(exc)

        logger.error(f"❌ Image processing failed for {image_id}")
        logger.error(f"   Error: {error_message}")
        logger.error(f"   Time before failure: {processing_time}ms")
        logger.exception("Full error traceback:")

        # Update database with error status
        update_image_in_database(image_id, {
            'processing_status': 'FAILED',
            'error_message': error_message,
            'processing_time_ms': processing_time
        })

        return {
            'success': False,
            'image_id': image_id,
            'error': error_message
        }
        if s3_client.upload_file(resolutions['ultra_hd'], ultra_hd_key, 'image/png'):
            s3_keys['ultra_hd'] = ultra_hd_key

        # Step 6: Update database with S3 keys and status (SYNC operation)
        print("Updating database...")
        _update_image_results_sync(
            image_id,
            s3_keys.get('small'),
            s3_keys.get('hd'),
            s3_keys.get('ultra_hd')
        )

        print(f"✓ Successfully processed image {image_id}")

        return {
            'success': True,
            'image_id': image_id,
            's3_keys': s3_keys,
            'message': 'Image processed successfully'
        }

    except Exception as exc:
        print(f"✗ Processing failed for image {image_id}: {exc}")
        import traceback
        traceback.print_exc()

        # Update status to FAILED
        try:
            _update_image_status_sync(image_id, 'FAILED', str(exc))
        except Exception as e:
            print(f"Failed to update error status: {e}")

        return {
            'success': False,
            'image_id': image_id,
            'error': str(exc)
        }


def _update_image_status_sync(
    image_id: str,
    status: str,
    error_message: Optional[str] = None
):
    """Update image processing status in database (SYNC using psycopg2)"""
    conn = None
    try:
        # Create synchronous connection
        database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql://").replace("postgresql+asyncpg://", "postgresql://")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        if error_message:
            cursor.execute(
                """
                UPDATE images
                SET processing_status = %s, error_message = %s
                WHERE id = %s
                """,
                (status, error_message, image_id)
            )
        else:
            cursor.execute(
                """
                UPDATE images
                SET processing_status = %s
                WHERE id = %s
                """,
                (status, image_id)
            )

        conn.commit()
        cursor.close()
        print(f"✓ Updated image {image_id} status to {status}")

    except Exception as e:
        print(f"✗ Failed to update image status: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def _update_image_results_sync(
    image_id: str,
    small_url: Optional[str],
    hd_url: Optional[str],
    ultra_hd_url: Optional[str]
):
    """Update image with processed S3 URLs (SYNC using psycopg2)"""
    conn = None
    try:
        # Create synchronous connection
        database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql://").replace("postgresql+asyncpg://", "postgresql://")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE images
            SET
                processing_status = 'COMPLETED',
                processed_small_url = %s,
                processed_hd_url = %s,
                processed_ultra_hd_url = %s,
                processed_at = NOW()
            WHERE id = %s
            """,
            (small_url, hd_url, ultra_hd_url, image_id)
        )

        conn.commit()
        cursor.close()
        print(f"✓ Updated image {image_id} with processed URLs")

    except Exception as e:
        print(f"✗ Failed to update image results: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
