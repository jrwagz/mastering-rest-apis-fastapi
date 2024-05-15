from logging.config import dictConfig


def configure_logging() -> None:
    """Configure Logging"""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(name)s:%(lineno)d - %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                }
            },
            "loggers": {
                "socialapi": {
                    "handlers": ["default"],
                    "level": "DEBUG",
                    "propagate": False,
                },
            },
        }
    )
