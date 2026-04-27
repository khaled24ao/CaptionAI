import logging
from typing import Optional


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Set up and configure a logger instance.
    
    Args:
        name: Logger name for identification.
        level: Logging level (defaults to INFO).
        
    Returns:
        Configured logger instance.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger(name)


app_logger = setup_logger("captionai")
ai_logger = setup_logger("captionai.ai")