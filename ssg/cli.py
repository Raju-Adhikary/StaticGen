import argparse
import logging
import os
import shutil

# Set up logging for informative messages (ensure this is at the top of the main script)
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Import functions from our new modules
from .config_loader import load_config
from .build_core import build_command
# Import load_plugins and run_hook. DO NOT import PLUGINS directly here.
from .plugin_system import load_plugins, run_hook 
from .dev_server import serve_command

# --- CLI Commands ---

def deploy_command(config_path):
    """Deploys the static site (placeholder)."""
    logger.info("Deploy command is a placeholder. Implement your deployment logic here.")
    config = load_config(config_path)
    config["config_path"] = config_path # Pass config_path
    
    # Load plugins before running deploy hook (populates PLUGINS in plugin_system.py)
    load_plugins(config) 
    run_hook("deploy", config=config) # This hook will use the global PLUGINS from plugin_system.py
    logger.info("Deploy command finished.")

def create_command(config_path):
    """Creates a new page or post (placeholder)."""
    logger.info("Create command is a placeholder. Implement your content creation logic here.")
    config = load_config(config_path)
    config["config_path"] = config_path # Pass config_path
    
    # Load plugins before running create_content hook (populates PLUGINS in plugin_system.py)
    load_plugins(config) 
    run_hook("create_content", config=config) # This hook will use the global PLUGINS from plugin_system.py
    logger.info("Create command finished.")

# --- Main CLI Entry Point ---

def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(description="A Python Static Site Generator.")
    parser.add_argument('--config', default='config.json', help='Path to the configuration file.')

    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # Build command
    build_parser = subparsers.add_parser('build', help='Builds the static site.')
    build_parser.set_defaults(func=build_command)

    # Serve command
    serve_parser = subparsers.add_parser('serve', help='Serves the site locally with live reloading.')
    serve_parser.add_argument('--port', type=int, default=8000, help='Port to serve the site on.')
    serve_parser.set_defaults(func=serve_command)

    # Deploy command (placeholder)
    deploy_parser = subparsers.add_parser('deploy', help='Deploys the static site.')
    deploy_parser.set_defaults(func=deploy_command)

    # Create command (placeholder)
    create_parser = subparsers.add_parser('create', help='Creates new content (e.g., page, post).')
    create_parser.set_defaults(func=create_command)

    args = parser.parse_args()

    # Call the function associated with the chosen command
    if args.command == 'serve':
        # Pass config_path to serve_command, which then passes it to build_command
        args.func(args.config, args.port) 
    else:
        # Pass config_path to other commands
        args.func(args.config)

if __name__ == "__main__":
    main()

