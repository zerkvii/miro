from typing import Generator
from loguru import logger

from app.core.config import settings

logger.add(settings.LOG_FILE,
           format=settings.LOG_FILE_FORMAT,
           compression=settings.LOG_FILE_COMPRESSION,
           rotation=settings.LOG_FILE_ROTATION,enqueue=True)


def get_logger() -> Generator:
    yield logger
