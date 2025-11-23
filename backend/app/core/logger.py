"""
Logging configuration using loguru
"""
from loguru import logger
import sys
from app.core.config import settings


def setup_logger():
    """Configure application logger"""

    # Remove default logger
    logger.remove()

    # Add console logger with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True,
    )

    # Add file logger for production
    if settings.ENVIRONMENT == "production":
        logger.add(
            "logs/bluepeak_{time:YYYY-MM-DD}.log",
            rotation="00:00",
            retention="30 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        )

    return logger


app_logger = setup_logger()
