import logging
import sys
from logging.config import dictConfig

def setup_logging():
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO"
        }
    }
    
    dictConfig(logging_config)
    return logging.getLogger(__name__)

logger = setup_logging()