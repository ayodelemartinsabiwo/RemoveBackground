"""
FastAPI health check endpoints
"""
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.core.redis import redis_client
from app.core.s3 import s3_client
from app.core.database import engine
from sqlalchemy import text
import asyncio

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """Basic health check - returns OK if service is running"""
    return {
        "status": "ok",
        "service": "palmar-bg-worker",
        "version": "1.0.0"
    }


@router.get("/ready")
async def readiness_check():
    """
    Readiness check - validates all dependencies are available
    Used by Kubernetes to determine if pod is ready to receive traffic
    """
    checks = {
        "redis": False,
        "s3": False,
        "database": False,
    }

    errors = []

    # Check Redis
    try:
        if redis_client.client:
            await redis_client.client.ping()
            checks["redis"] = True
        else:
            errors.append("Redis client not initialized")
    except Exception as e:
        errors.append(f"Redis: {str(e)}")

    # Check S3
    try:
        if s3_client.client:
            # Try to list buckets as a connectivity test
            s3_client.client.list_buckets()
            checks["s3"] = True
        else:
            errors.append("S3 client not initialized")
    except Exception as e:
        errors.append(f"S3: {str(e)}")

    # Check Database
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            checks["database"] = True
    except Exception as e:
        errors.append(f"Database: {str(e)}")

    # Determine overall readiness
    all_ready = all(checks.values())

    response_data = {
        "ready": all_ready,
        "checks": checks,
    }

    if errors:
        response_data["errors"] = errors

    status_code = status.HTTP_200_OK if all_ready else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(content=response_data, status_code=status_code)


@router.get("/live")
async def liveness_check():
    """
    Liveness check - simple check to see if process is alive
    Used by Kubernetes to determine if pod should be restarted
    """
    return {"alive": True}
