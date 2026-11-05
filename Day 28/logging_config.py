
import logging
import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# Create the logs directory
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )


def get_logger(name):
    return logging.getLogger(name)
