import yaml
from pathlib import Path
import os

def load_config(config_path: str) -> dict:
    path=Path(config_path)
    if not path.exists():
        raise FileNotFoundError("Config file not found. {path}")
    with open(path, 'r',encoding="utf-8") as file:
        return yaml.safe_load(file) or {}