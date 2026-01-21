import json
import logging

logger = logging.getLogger(__name__)

def load_config(config_path):
    """Loads configuration settings from a specified JSON file."""
    logger.info("Loading configuration from %s", config_path)
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from config file {config_path}: {e}")
        raise

