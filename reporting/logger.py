import logging
import os
from datetime import datetime


def setup_logger(email_id):
    # Create logs directory if not exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/email_{email_id}_{timestamp}.log"

    # Create logger
    logger = logging.getLogger(email_id)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(log_filename)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger