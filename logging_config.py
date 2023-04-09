import os
import socket

from dotenv import load_dotenv
load_dotenv()

SERVICE_NAME = os.getenv("SERVICE_NAME")
SERVICE_ENV = os.getenv("SERVICE_ENV")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "papertrail": {
            "format": f"%(asctime)s - {SERVICE_NAME}_{SERVICE_ENV} - %(levelname)s - %(name)s - %(message)s",
            "datefmt": '%Y-%m-%d %H:%M:%S %Z',
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "papertrail",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    }
}
