import yaml
from pathlib import Path
import os
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException


def load_config(config_path: str) -> dict:
    try:
        path=Path(config_path)
        if not path.exists():
            raise FileNotFoundError("Config file not found. {path}")
        log.info(f"Loading configuration from {config_path}")
        with open(path, 'r',encoding="utf-8") as file:
            return yaml.safe_load(file) or {}
    except Exception as e:
        log.error(f"Error in while loading config_loader: {e}")
        raise CustomException(e)
