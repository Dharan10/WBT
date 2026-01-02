import sys
from loguru import logger
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure Loguru to JSON
def setup_logging():
    logger.remove()  # Remove default handler
    
    # Console handler (Human readable for dev)
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    # File handler (JSON for machine parsing)
    logger.add(
        LOG_DIR / "wbt.json",
        serialize=True,
        level="DEBUG",
        rotation="10 MB",
        retention="10 days"
    )

setup_logging()
