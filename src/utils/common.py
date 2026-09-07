import os
import sys
import yaml
from pathlib import Path
from src.exception.exception import MarketException
from src.logging.logger import logging

def read_yaml(file_path: str | Path) -> dict:
    """Reads a YAML file and returns its content as a dictionary."""
    try:
        with open(file_path, "r", encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"Loaded YAML file successfully from: {file_path}")
            return content
    except Exception as e:
        raise MarketException(e, sys) from e

def write_yaml(file_path: str | Path, content: object, replace: bool = False) -> None:
    """Writes content to a YAML file."""
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(content, file)
            logging.info(f"Written YAML file successfully to: {file_path}")
    except Exception as e:
        raise MarketException(e, sys) from e

def create_directories(path_to_directories: list, verbose=True):
    """Creates a list of directories if they do not exist."""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging.info(f"Created directory at: {path}")