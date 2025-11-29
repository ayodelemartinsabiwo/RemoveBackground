"""
Core module initialization
"""
from app.core.config import settings
from app.core.redis import redis_client
from app.core.s3 import s3_client
from app.core.database import get_db, init_db, close_db

__all__ = [
    "settings",
    "redis_client",
    "s3_client",
    "get_db",
    "init_db",
    "close_db",
]
