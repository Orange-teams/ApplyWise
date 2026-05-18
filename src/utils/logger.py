import logging
from pathlib import Path

from config.settings import settings


def setup_logger():

    # Ensure log directory exists
    settings.LOG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_file = settings.LOG_DIR / "app.log"

    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )