"""
Configuration using Pydantic Settings
Loads from environment variables with validation
"""
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable loading"""

    # Application
    APP_NAME: str = "Palmar Background Removal Worker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, validation_alias="DEBUG")

    # Redis
    REDIS_HOST: str = Field(default="localhost", validation_alias="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, validation_alias="REDIS_PORT")
    REDIS_PASSWORD: Optional[str] = Field(default=None, validation_alias="REDIS_PASSWORD")
    REDIS_DB: int = Field(default=0, validation_alias="REDIS_DB")

    @property
    def REDIS_URL(self) -> str:
        """Construct Redis URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # Celery
    CELERY_BROKER_URL: Optional[str] = Field(default=None, validation_alias="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: Optional[str] = Field(default=None, validation_alias="CELERY_RESULT_BACKEND")

    @property
    def celery_broker(self) -> str:
        """Get Celery broker URL"""
        return self.CELERY_BROKER_URL or self.REDIS_URL

    @property
    def celery_backend(self) -> str:
        """Get Celery result backend URL"""
        return self.CELERY_RESULT_BACKEND or self.REDIS_URL

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/palmar_bg",
        validation_alias="DATABASE_URL"
    )

    # S3/MinIO
    S3_ENDPOINT: Optional[str] = Field(default=None, validation_alias="S3_ENDPOINT")
    S3_ACCESS_KEY: str = Field(default="minioadmin", validation_alias="S3_ACCESS_KEY")
    S3_SECRET_KEY: str = Field(default="minioadmin", validation_alias="S3_SECRET_KEY")
    S3_BUCKET_NAME: str = Field(default="palmar-bg-images", validation_alias="S3_BUCKET_NAME")
    S3_REGION: str = Field(default="us-east-1", validation_alias="S3_REGION")
    S3_USE_SSL: bool = Field(default=True, validation_alias="S3_USE_SSL")

    # AI Model Settings
    MODEL_NAME: str = Field(default="birefnet-portrait", validation_alias="MODEL_NAME")
    MODEL_FALLBACK: str = Field(default="u2net", validation_alias="MODEL_FALLBACK")
    MAX_IMAGE_SIZE: int = Field(default=1024, validation_alias="MAX_IMAGE_SIZE")

    # Processing Settings
    SMALL_RESOLUTION: int = Field(default=512, validation_alias="SMALL_RESOLUTION")
    HD_RESOLUTION: int = Field(default=1920, validation_alias="HD_RESOLUTION")
    ULTRA_HD_RESOLUTION: int = Field(default=3840, validation_alias="ULTRA_HD_RESOLUTION")

    # Worker Settings
    WORKER_CONCURRENCY: int = Field(default=2, validation_alias="WORKER_CONCURRENCY")
    TASK_TIME_LIMIT: int = Field(default=300, validation_alias="TASK_TIME_LIMIT")  # 5 minutes
    TASK_SOFT_TIME_LIMIT: int = Field(default=240, validation_alias="TASK_SOFT_TIME_LIMIT")  # 4 minutes

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
