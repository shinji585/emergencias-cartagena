import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

BASE_DIR = Path(__file__).resolve().parents[3]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = None
try:
    file_handler = RotatingFileHandler(
        str(LOG_FILE), maxBytes=10_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
except PermissionError:
    file_handler = None

logger = logging.getLogger("emergencias_cartagena")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
if file_handler is not None:
    logger.addHandler(file_handler)
