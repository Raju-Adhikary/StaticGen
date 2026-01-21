import os
import logging
import datetime
import http.server
import socketserver
import threading
import mimetypes

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .build_core import build_command
from .config_loader import load_config
from .plugin_system import load_plugins, run_hook

logger = logging.getLogger(__name__)

class MyHandler(FileSystemEventHandler):
    """Handles file system events for the watch mode."""
    def __init__(self, config_path_arg):
        super().__init__()
        self.config_path = config_path_arg
        self.last_rebuild_time = datetime.datetime.now()
        self.config = load_config(config_path_arg) # Load config once for event handler

    def on_any_event(self, event):
        # Debounce rebuilds to avoid multiple rapid rebuilds for single save operations
        if datetime.datetime.now() - self.last_rebuild_time < datetime.timedelta(seconds=1):
            return

        # Only rebuild on changes to relevant directories
        relevant_dirs = [
            self.config['pages_dir'],
            self.config['templates_dir'],
            self.config['static_dir'],
            self.config['assets_dir'],
            self.config.get('data_dir'),
            self.config.get('plugins_dir')
        ]
        # Add collection paths
        for coll_settings in self.config.get('collections', {}).values():
            relevant_dirs.append(coll_settings.get('path'))
        
        # Filter out None values and ensure paths are absolute for comparison
        relevant_dirs = [os.path.abspath(d) for d in relevant_dirs if d and os.path.exists(d)]
        
        event_path_abs = os.path.abspath(event.src_path)

        if any(event_path_abs.startswith(d) for d in relevant_dirs) or event_path_abs == os.path.abspath(self.config_path):
            logger.info(f"Detected change in {event.src_path}. Rebuilding................................................")
            try:
                build_command(self.config_path) # This call will handle plugin loading internally
                self.last_rebuild_time = datetime.datetime.now()
                logger.info("Rebuild complete. Refresh your browser to see changes.")
            except Exception as e:
                logger.error(f"Error during rebuild: {e}")

def serve_command(config_path, port=8000):
    """Starts a local development server with live reloading."""
    config = load_config(config_path)
    output_dir = config["output_dir"]

    # Initial build (this will call build_command which handles plugin loading)
    build_command(config_path)

    # Start file system observer
    event_handler = MyHandler(config_path)
    observer = Observer()
    
    # Watch all relevant directories
    dirs_to_watch = [
        config['pages_dir'],
        config['templates_dir'],
        config['static_dir'],
        config['assets_dir'],
        config.get('data_dir'),
        config.get('plugins_dir')
    ]
    for coll_settings in config.get('collections', {}).values():
        dirs_to_watch.append(coll_settings.get('path'))

    # Add config file itself to watch
    dirs_to_watch.append(os.path.dirname(config_path))

    for d in dirs_to_watch:
        if d and os.path.exists(d):
            observer.schedule(event_handler, d, recursive=True)
    
    observer.start()
    logger.info(f"Watching for changes in: {', '.join([d for d in dirs_to_watch if d])}")

    # Start HTTP server
    class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=output_dir, **kwargs)

        def do_GET(self):
            # This method is called for GET requests.
            # It will try to serve the requested path.
            # If a directory is requested (e.g., /blog/), it will look for index.html inside it.
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()

        def send_head(self):
            # This method prepares the response headers and returns a file object.
            # It handles path translation and checks for index.html in directories.
            path = self.translate_path(self.path)
            f = None
            if os.path.isdir(path):
                # If a directory is requested, look for index.html within it
                index_path = os.path.join(path, 'index.html')
                if os.path.exists(index_path):
                    path = index_path
                else:
                    # If no index.html, return 404. We don't want directory listings.
                    self.send_error(404, "Directory listing not supported or index.html not found")
                    return None
            
            # Check if the file exists and is a regular file
            if not os.path.exists(path) or not os.path.isfile(path):
                self.send_error(404, "File not found")
                return None

            ctype = self.guess_type(path)
            try:
                f = open(path, 'rb')
            except OSError:
                self.send_error(404, "File not found") # Should be caught by os.path.exists already
                return None
            
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f

        def guess_type(self, path):
            """Guess the type of a file. Extension based."""
            base, ext = os.path.splitext(path)
            if ext in self.extensions_map:
                return self.extensions_map[ext]
            ext = ext.lower()
            if ext in self.extensions_map:
                return self.extensions_map[ext]
            else:
                return 'application/octet-stream'

        # Add common extensions for better MIME type handling
        extensions_map = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.txt': 'text/plain',
            '.ico': 'image/x-icon',
            '.pdf': 'application/pdf',
            '.woff': 'font/woff',
            '.woff2': 'font/woff2',
            '.ttf': 'font/ttf',
            '.eot': 'application/vnd.ms-fontobject',
            '.otf': 'font/otf',
        }
        mimetypes.add_type('application/javascript', '.js')
        mimetypes.add_type('image/svg+xml', '.svg')


    # Use ThreadingTCPServer to allow graceful shutdown and avoid blocking
    Handler = SimpleHTTPRequestHandler
    httpd = socketserver.ThreadingTCPServer(("", port), Handler)

    logger.info(f"Serving site at http://localhost:{port}/")
    logger.info("Press Ctrl+C to stop the server and watcher.")
    
    # Run the server in a separate thread to allow the observer to run
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True # Allow main program to exit even if thread is running
    server_thread.start()

    try:
        while True:
            # Keep main thread alive
            threading.Event().wait(1)
    except KeyboardInterrupt:
        logger.info("Stopping server and watcher...")
        httpd.shutdown()
        observer.stop()
        observer.join()
        logger.info("Server and watcher stopped.")

