from logging import Logger, getLogger
from logging import DEBUG
from pathlib import Path
from logging.config import dictConfig

from yaml import safe_load

class LoggerBuilder:
    def __init__(self, name: str, level: int = DEBUG):
        self._name = name
        self._level = level

    def from_yaml(self, filepath: Path) -> Logger:
        with open(filepath, 'r') as f:
            config = safe_load(f.read())
        dictConfig(config)

        return getLogger(self._name)
    