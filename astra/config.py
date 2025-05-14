import json
import os
import logging

def load_config(config_path: str) -> dict:
    """Load configuration from a JSON file."""
    config_path = os.path.expanduser(config_path)
    if not os.path.exists(config_path):
        logging.debug(f"Config file {config_path} not found.")
        return {}
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        logging.debug(f"Loaded config from {config_path}")
        return config
    except Exception as e:
        logging.error(f"Error loading config from {config_path}: {e}")
        return {}
