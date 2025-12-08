"""
FastAPI application for Python AI Worker
Provides health check endpoints and initializes connections
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import health_router
from app.api.process import router as process_router
from app.api.trigger import router as celery_router
from app.core import redis_client, s3_client, init_db, close_db, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events"""
    # Startup
    print("🚀 Starting Palmar BG Worker...")

    # Initialize Redis
    try:
        await redis_client.connect()
    except Exception as e:
        print(f"Warning: Redis connection failed: {e}")

    # Initialize S3
    try:
        s3_client.connect()
    except Exception as e:
        print(f"Warning: S3 connection failed: {e}")

    # Initialize Database
    try:
        await init_db()
    except Exception as e:
        print(f"Warning: Database connection failed: {e}")

    print("✓ Worker ready to process images!")

    yield

    # Shutdown
    print("Shutting down worker...")

    try:
        await redis_client.disconnect()
    except:
        pass

    try:
        await close_db()
    except:
        pass

    print("✓ Worker shut down successfully")


# Create FastAPI app
app = FastAPI(
    title="Palmar Background Removal Worker",
    description="Python AI Worker for background removal processing",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(process_router)
app.include_router(celery_router)  # Celery trigger endpoint


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Palmar Background Removal Worker",
        "version": "1.0.0",
        "status": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG,
    )
