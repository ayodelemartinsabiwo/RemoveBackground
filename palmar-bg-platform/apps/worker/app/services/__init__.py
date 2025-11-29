"""
Services module initialization
"""
from app.services.background_removal import BackgroundRemovalService
from app.services.image_optimization import ImageOptimizationService
from app.services.background_editor import BackgroundEditorService

__all__ = [
    "BackgroundRemovalService",
    "ImageOptimizationService",
    "BackgroundEditorService",
]
