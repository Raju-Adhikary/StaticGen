import os
import logging
import sys

logger = logging.getLogger(__name__)

# Global list to store loaded plugins. This is the SINGLE source of truth.
PLUGINS = []

def load_plugins(config):
    """
    Loads Python modules from the plugins directory and populates the global PLUGINS list.
    This function is responsible for managing the PLUGINS list.
    """
    global PLUGINS # Declare intent to modify the global PLUGINS list
    
    plugins_dir = config.get("plugins_dir")
    
    # Clear existing plugins to ensure a fresh load on rebuilds
    PLUGINS.clear() 

    if not plugins_dir or not os.path.exists(plugins_dir):
        logger.info("No plugins directory found or specified. Skipping plugin loading.")
        return [] # Return an empty list if no plugins

    logger.info(f"Loading plugins from {plugins_dir}")
    
    # Add plugins directory to Python path temporarily
    sys.path.insert(0, plugins_dir)

    for file_name in os.listdir(plugins_dir):
        if file_name.endswith(".py") and not file_name.startswith("__"):
            module_name = file_name[:-3]
            try:
                # Import the module dynamically
                module = __import__(module_name)
                PLUGINS.append(module) # Directly append to the global PLUGINS list
                logger.info(f"Loaded plugin: {module_name}")
            except Exception as e:
                logger.error(f"Error loading plugin {module_name}: {e}")
    
    # Remove plugins directory from path after loading
    sys.path.pop(0) 
    return PLUGINS # Return the global list (optional, but good for consistency)

def run_hook(hook_name, *args, **kwargs):
    """
    Runs a specified hook across all loaded plugins.
    It accesses the global PLUGINS list managed by load_plugins.
    """
    # No 'global PLUGINS' needed here if PLUGINS is only read.
    # If it were modified, 'global PLUGINS' would be needed.
    for plugin in PLUGINS:
        if hasattr(plugin, hook_name) and callable(getattr(plugin, hook_name)):
            try:
                getattr(plugin, hook_name)(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error running hook '{hook_name}' in plugin '{plugin.__name__}': {e}")
