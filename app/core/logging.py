import os
from loguru import logger
from app.core.config import settings

def setup_logging():
    logger.remove()

    os.makedirs("logs", exist_ok=True)

    
    logger.add(
    settings.log_file_path,
    level=settings.log_level,
    rotation=settings.log_rotation,
    retention=settings.log_retention,
    compression="zip",
    serialize=settings.log_format_json,  
    enqueue=True,  
    )
   