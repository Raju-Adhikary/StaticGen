import json
import logging

logger = logging.getLogger(__name__)

def parse_front_matter(content):
    """
    Parses JSON front matter from the beginning of a string.
    Expects front matter to be enclosed by '+++' lines.
    Returns a tuple: (front_matter_dict, content_without_front_matter)
    """
    if content.startswith('+++'):
        parts = content.split('+++', 2)
        if len(parts) > 2:
            try:
                front_matter = json.loads(parts[1])
                return front_matter if front_matter else {}, parts[2].strip()
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON front matter: {e}")
                return {}, content
    return {}, content

