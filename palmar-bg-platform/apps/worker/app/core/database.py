"""
Async database connection using SQLAlchemy
"""
import logging
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, text
from app.core.config import settings

logger = logging.getLogger(__name__)

# Convert postgres:// to postgresql+asyncpg://
database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine with better connection handling
engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,
    pool_size=10,  # Increased pool size
    max_overflow=20,  # Increased overflow
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_timeout=30,  # Wait up to 30s for connection
    connect_args={
        "server_settings": {"jit": "off"},  # Disable JIT for stability
        "timeout": 10,  # Connection timeout
        "command_timeout": 60,  # Command timeout
    },
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database connection"""
    try:
        from sqlalchemy import text
        async with engine.begin() as conn:
            # Test connection
            await conn.execute(text("SELECT 1"))
        print("✓ Connected to database")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        raise


async def close_db():
    """Close database connection"""
    await engine.dispose()
    print("✓ Closed database connection")


# Synchronous database operations for Celery workers
def update_image_in_database(image_id: str, update_data: Dict) -> bool:
    """
    Update image record directly in database (bypasses API authentication)

    This solves the issue where worker can't call PATCH /api/v1/images/:id
    because it requires user authentication.

    Args:
        image_id: UUID of the image
        update_data: Dict containing fields to update:
            - processed_s3_key: S3 key of processed image (main field)
            - processed_small_url: S3 key for small version (used by API)
            - processed_hd_url: S3 key for HD version
            - processed_ultra_hd_url: S3 key for Ultra HD version
            - processing_status: PENDING | PROCESSING | COMPLETED | FAILED
            - processing_time_ms: Time taken in milliseconds
            - processed_file_size: Size of processed file in bytes
            - error_message: Error message if failed

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Use synchronous engine for Celery workers
        sync_engine = create_engine(settings.DATABASE_URL)

        with sync_engine.begin() as conn:
            # Build update query dynamically based on provided fields
            update_fields = []
            params = {'image_id': image_id}

            if 'processed_s3_key' in update_data:
                update_fields.append('processed_s3_key = :processed_s3_key')
                params['processed_s3_key'] = update_data['processed_s3_key']

            # Support for multi-resolution URLs (used by API for presigned URL generation)
            if 'processed_small_url' in update_data:
                update_fields.append('processed_small_url = :processed_small_url')
                params['processed_small_url'] = update_data['processed_small_url']

            if 'processed_hd_url' in update_data:
                update_fields.append('processed_hd_url = :processed_hd_url')
                params['processed_hd_url'] = update_data['processed_hd_url']

            if 'processed_ultra_hd_url' in update_data:
                update_fields.append('processed_ultra_hd_url = :processed_ultra_hd_url')
                params['processed_ultra_hd_url'] = update_data['processed_ultra_hd_url']

            if 'processing_status' in update_data:
                # Cast to enum type for PostgreSQL
                update_fields.append('processing_status = CAST(:processing_status AS "ProcessingStatus")')
                params['processing_status'] = update_data['processing_status']

            if 'processing_time_ms' in update_data:
                update_fields.append('processing_time_ms = :processing_time_ms')
                params['processing_time_ms'] = update_data['processing_time_ms']

            if 'processed_file_size' in update_data:
                update_fields.append('processed_file_size = :processed_file_size')
                params['processed_file_size'] = update_data['processed_file_size']

            if 'error_message' in update_data:
                update_fields.append('error_message = :error_message')
                params['error_message'] = update_data['error_message']

            # Always update processed_at timestamp when updating
            update_fields.append('processed_at = NOW()')

            if not update_fields:
                logger.warning(f"⚠️ No fields to update for image {image_id}")
                return False

            query = text(f"""
                UPDATE images
                SET {', '.join(update_fields)}
                WHERE id = :image_id
                RETURNING id
            """)

            result = conn.execute(query, params)
            row = result.fetchone()

            if row:
                logger.info(f"✅ Successfully updated image {image_id} in database")
                logger.info(f"   Updated fields: {list(update_data.keys())}")
                return True
            else:
                logger.error(f"❌ No rows updated for image {image_id} - image may not exist")
                return False

    except Exception as e:
        logger.error(f"❌ Failed to update image {image_id} in database: {e}")
        logger.exception("Full error:")
        return False


def get_image_from_database(image_id: str) -> Optional[Dict]:
    """
    Get image record from database

    Args:
        image_id: UUID of the image

    Returns:
        dict: Image data or None if not found
    """
    try:
        sync_engine = create_engine(settings.DATABASE_URL)

        with sync_engine.connect() as conn:
            query = text("""
                SELECT
                    id, user_id, original_filename, original_s3_key,
                    processed_s3_key, processing_status, processing_time_ms,
                    processed_file_size, error_message, created_at, processed_at
                FROM images
                WHERE id = :image_id
            """)

            result = conn.execute(query, {'image_id': image_id})
            row = result.fetchone()

            if row:
                return dict(row._mapping)
            return None

    except Exception as e:
        logger.error(f"❌ Failed to get image {image_id} from database: {e}")
        return None
