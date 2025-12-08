"""
Image processing API endpoint
Receives requests from BullMQ worker and processes images
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.tasks.process_image import process_image_task
from app.core.database import AsyncSessionLocal
from sqlalchemy import text
import asyncio

router = APIRouter(prefix="/api", tags=["processing"])


class ProcessImageRequest(BaseModel):
    """Request model for image processing"""
    image_id: str
    user_id: str
    s3_key: str
    background_type: Optional[str] = "TRANSPARENT"
    background_config: Optional[Dict[str, Any]] = None
    download_tier: Optional[str] = "SMALL"


class ProcessImageResponse(BaseModel):
    """Response model for image processing"""
    success: bool
    message: str
    image_id: str
    processed_small_url: Optional[str] = None
    processed_hd_url: Optional[str] = None
    processed_ultra_hd_url: Optional[str] = None
    processed_s3_key: Optional[str] = None


@router.post("/process", response_model=ProcessImageResponse)
async def process_image(request: ProcessImageRequest):
    """
    Process an image with background removal

    This endpoint is called by the BullMQ worker (Node.js) to process images.
    It runs the Celery task synchronously and returns the result.
    """
    try:
        print(f"📥 Received processing request for image {request.image_id}")

        # Convert background_type to background_options format
        background_options = None
        if request.background_type and request.background_type != "TRANSPARENT":
            background_options = {
                "type": request.background_type.lower()
            }

            # Add config if provided
            if request.background_config:
                background_options.update(request.background_config)

        # Call the SYNC task function via ThreadPoolExecutor
        # This prevents blocking the event loop with sync I/O (boto3, rembg, PIL)
        from app.tasks.process_image_sync import process_image_sync
        from concurrent.futures import ThreadPoolExecutor

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                process_image_sync,
                request.image_id,
                request.user_id,
                request.s3_key,
                background_options
            )

        if result.get('success'):
            s3_keys = result.get('s3_keys', {})

            return ProcessImageResponse(
                success=True,
                message="Image processed successfully",
                image_id=request.image_id,
                processed_small_url=s3_keys.get('small'),
                processed_hd_url=s3_keys.get('hd'),
                processed_ultra_hd_url=s3_keys.get('ultra_hd'),
                processed_s3_key=s3_keys.get('small')  # Primary key is small version
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get('error', 'Processing failed')
            )

    except Exception as e:
        print(f"❌ Processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{image_id}")
async def get_processing_status(image_id: str):
    """
    Get the current processing status of an image
    """
    try:
        async with AsyncSessionLocal() as session:
            query = text("""
                SELECT
                    id,
                    processing_status,
                    processed_small_url,
                    processed_hd_url,
                    processed_ultra_hd_url,
                    error_message
                FROM images
                WHERE id = :image_id
            """)

            result = await session.execute(query, {"image_id": image_id})
            row = result.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Image not found")

            return {
                "id": row[0],
                "processingStatus": row[1],
                "processedSmallUrl": row[2],
                "processedHdUrl": row[3],
                "processedUltraHdUrl": row[4],
                "errorMessage": row[5]
            }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
