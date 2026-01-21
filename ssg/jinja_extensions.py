from jinja2 import nodes
from jinja2.ext import Extension
import datetime
import logging

from .url_helpers import url, static

logger = logging.getLogger(__name__)

class TagExtension(Extension):
    """
    A Jinja2 extension to add custom tags: 'static', 'url', and 'now'.
    These tags process their arguments to generate appropriate paths or timestamps.
    """
    tags = ['static','url','now']

    def __init__(self, environment):
        super().__init__(environment)

    def parse(self, parser):
        """Parses the custom tags and calls the appropriate handler methods."""
        token = next(parser.stream)
        lineno = token.lineno
        if token.value == 'static':
            args = [parser.parse_expression()]
            return nodes.Output([self.call_method('_static', args)]).set_lineno(lineno)
        elif token.value == 'url':
            args = [parser.parse_expression()]
            return nodes.Output([self.call_method('_url', args)]).set_lineno(lineno)
        elif token.value == 'now':
            # Optionally parse an argument for format string
            args = [parser.parse_expression()] if not parser.stream.current.test('block_end') else []
            return nodes.Output([self.call_method('_now', args)]).set_lineno(lineno)

    def _static(self, path):
        """Internal handler for the 'static' tag, calls the static helper."""
        config = self.environment.globals['site']['config'] # Access config from environment globals
        return static(path, config)
        
    def _url(self, path):
        """Internal handler for the 'url' tag, calls the url helper."""
        config = self.environment.globals['site']['config'] # Access config from environment globals
        return url(path, config)
    
    def _now(self, format_string="%Y-%m-%d %H:%M:%S"):
        """Internal handler for the 'now' tag, displays current date/time."""
        # Check if format_string is a Jinja2 node (e.g., nodes.Const) and extract its value
        if hasattr(format_string, 'value'):
            format_string = format_string.value
        elif not isinstance(format_string, str): # Default if not a string or node
            format_string = "%Y-%m-%d %H:%M:%S"
        return datetime.datetime.now().strftime(format_string)

