"""
Tasks module initialization
"""
from app.tasks.celery_app import celery_app
from app.tasks.process_image import process_image_task

__all__ = ["celery_app", "process_image_task"]
