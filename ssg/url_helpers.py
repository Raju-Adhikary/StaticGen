import os
import logging

logger = logging.getLogger(__name__)

def url(path, config):
    """Generates a URL based on the provided path and configuration."""
    if config.get("use_absolute_urls"):
        return f"{config['base_url']}/{path.lstrip('/')}"
    return f"/{path.lstrip('/')}"

def static(path, config):
    """Generates a static file path, with an optional check for file existence."""
    static_path = os.path.join(config["static_dir"], path.lstrip('/'))
    if not os.path.exists(static_path):
        logger.warning("Static file not found: %s", static_path)
    
    if config.get("use_absolute_static"):
        return f"{config['base_url']}/static/{path.lstrip('/')}"
    return f"/static/{path.lstrip('/')}"

