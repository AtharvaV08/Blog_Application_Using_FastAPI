import logging
from logging import Logger
from pathlib import Path
import os


class BasicLogger:
    """Centralized logger factory for consistent application logging."""

    _instances = {}

    def __new__(cls, name: str = "app", log_file: str | None = None, level: int = logging.INFO):
        key = (name, log_file, level)
        if key not in cls._instances:
            cls._instances[key] = super().__new__(cls)
        return cls._instances[key]

    def __init__(self, name: str = "app", log_file: str | None = None, level: int = logging.INFO):
        if getattr(self, "_initialized", False):
            return

        if not os.path.exists(os.path.join(os.getcwd(), "logs")):
            os.makedirs(os.path.join(os.getcwd(), "logs"))

        self.name = name
        self.level = level
        self.log_file = os.path.join(os.getcwd(), "logs", log_file) if log_file else "logs/app.log"
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

            if log_file:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_path, encoding="utf-8")
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

        self._initialized = True

    def get_logger(self) -> Logger:
        """Return the configured logger instance."""
        return self.logger


def get_logger(name: str = "app", log_file: str | None = None, level: int = logging.INFO) -> Logger:
    """Convenience helper to fetch a centralized logger."""
    return BasicLogger(name=name, log_file=log_file, level=level).get_logger()
