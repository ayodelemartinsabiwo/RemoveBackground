"""
Celery Task Trigger API
Lightweight HTTP endpoint for triggering Celery tasks from Node.js API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
import os

# Add parent directory to path to import celery_tasks
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from celery_tasks import process_image_task, health_check_task
    from celery_app import celery_app
except ImportError as e:
    print(f"Warning: Could not import Celery tasks: {e}")
    print("Celery functionality will not be available")
    process_image_task = None
    health_check_task = None
    celery_app = None

router = APIRouter(prefix="/api/celery", tags=["celery"])


class TriggerImageProcessingRequest(BaseModel):
    """Request model for triggering image processing"""
    image_id: str
    user_id: str
    s3_key: str
    background_type: Optional[str] = "TRANSPARENT"
    background_config: Optional[Dict[str, Any]] = None


class TriggerImageProcessingResponse(BaseModel):
    """Response model for triggering image processing"""
    success: bool
    message: str
    task_id: str
    image_id: str


class TaskStatusResponse(BaseModel):
    """Response model for task status"""
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.post("/trigger", response_model=TriggerImageProcessingResponse)
async def trigger_image_processing(request: TriggerImageProcessingRequest):
    """
    Trigger Celery task for image processing

    This endpoint is called by the Node.js API to trigger image processing.
    It queues the task in Celery and returns immediately with the task ID.
    """
    if not process_image_task or not celery_app:
        raise HTTPException(
            status_code=503,
            detail="Celery is not available. Worker may be starting up."
        )

    try:
        print(f"📤 Triggering Celery task for image {request.image_id}")

        # Trigger Celery task (returns immediately with task ID)
        task = process_image_task.apply_async(
            args=[
                request.image_id,
                request.user_id,
                request.s3_key,
                request.background_type,
                request.background_config
            ],
            task_id=request.image_id,  # Use image ID as task ID for idempotency
        )

        print(f"✓ Celery task queued: {task.id}")

        return TriggerImageProcessingResponse(
            success=True,
            message="Image processing task queued successfully",
            task_id=task.id,
            image_id=request.image_id
        )

    except Exception as e:
        print(f"✗ Failed to trigger Celery task: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to queue image processing task: {str(e)}"
        )


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Get Celery task status

    Returns the current status of a Celery task by its ID.
    """
    if not celery_app:
        raise HTTPException(
            status_code=503,
            detail="Celery is not available"
        )

    try:
        # Get task result
        task_result = celery_app.AsyncResult(task_id)

        # Get task state and result
        status = task_result.state
        result = None
        error = None

        if status == 'SUCCESS':
            result = task_result.result
        elif status == 'FAILURE':
            error = str(task_result.result)

        return TaskStatusResponse(
            task_id=task_id,
            status=status,
            result=result,
            error=error
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get task status: {str(e)}"
        )


@router.get("/health")
async def celery_health_check():
    """
    Check if Celery worker is healthy

    Triggers a simple health check task to verify worker is running.
    """
    if not health_check_task or not celery_app:
        return {
            "status": "unavailable",
            "message": "Celery is not configured"
        }

    try:
        # Trigger health check task with 5 second timeout
        result = health_check_task.apply_async().get(timeout=5)
        return {
            "status": "healthy",
            "celery": result
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
