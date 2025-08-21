# app/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Create logger
logger = logging.getLogger("library_logger")
logger.setLevel(logging.INFO)  # or DEBUG for more details

# Create a file handler with rotation
file_handler = RotatingFileHandler("logs/app.log", maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

