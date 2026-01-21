import os
import json
import logging

from .front_matter_parser import parse_front_matter
from .url_helpers import url

logger = logging.getLogger(__name__)

def load_data_files(config):
    """
    Loads data from JSON files in the 'data_dir' (e.g., _data).
    Data is made available under `site.data` in Jinja2.
    """
    data = {}
    data_dir = config.get("data_dir")
    if not data_dir or not os.path.exists(data_dir):
        logger.info("No data directory found or specified. Skipping data loading.")
        return data

    logger.info(f"Loading data files from {data_dir}")
    for root, _, files in os.walk(data_dir):
        for file_name in files:
            name, ext = os.path.splitext(file_name)
            if ext.lower() == '.json': # Only load .json files
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(file_path, data_dir)
                # Create nested dictionary structure based on path
                keys = name.split(os.sep)
                current_data_node = data
                for key in keys[:-1]:
                    current_data_node = current_data_node.setdefault(key, {})
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        current_data_node[keys[-1]] = json.load(f)
                    logger.info(f"Loaded data: {relative_path}")
                except Exception as e:
                    logger.error(f"Error loading data file {file_path}: {e}")
            else:
                logger.warning(f"Skipping non-JSON data file: {file_name}")
    return data

def load_collections(config):
    """
    Loads content from defined collections.
    Each collection item will have its front matter parsed.
    Only HTML files are considered.
    """
    collections_data = {}
    collections_config = config.get("collections", {})

    for collection_name, collection_settings in collections_config.items():
        collection_path = collection_settings.get("path")
        if not collection_path or not os.path.exists(collection_path):
            logger.warning(f"Collection '{collection_name}' path not found: {collection_path}. Skipping.")
            continue

        logger.info(f"Loading collection: {collection_name} from {collection_path}")
        items = []
        for root, _, files in os.walk(collection_path):
            for file_name in files:
                if file_name.endswith('.html'): # Only process HTML files
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    front_matter, body_content = parse_front_matter(content)
                    
                    # Determine output path for collection item
                    relative_path = os.path.relpath(file_path, collection_path)
                    output_dir_name = collection_settings.get("output", collection_name)
                    
                    # Collection items will now also retain their original filename.html in the output.
                    output_file_name = relative_path 

                    item_output_path = os.path.join(output_dir_name, output_file_name)
                    
                    item = {
                        "path": file_path,
                        "relative_path": relative_path,
                        "output_path_relative": item_output_path,
                        "front_matter": front_matter,
                        "content": body_content, # Raw content after front matter
                        "url": url(item_output_path, config) # Absolute URL for the item
                    }
                    items.append(item)
        collections_data[collection_name] = items
    return collections_data

