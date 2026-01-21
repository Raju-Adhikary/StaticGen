import os
import shutil
import logging
import datetime
import json
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from jinja2 import Environment, FileSystemLoader

# Import necessary components from other modules
from .front_matter_parser import parse_front_matter
from .url_helpers import url, static # Ensure 'static' is imported here if used globally, or passed
from .jinja_extensions import TagExtension
from .plugin_system import run_hook, load_plugins
from .config_loader import load_config
from .data_collections_loader import load_data_files, load_collections

logger = logging.getLogger(__name__)

def setup_jinja_environment(config, site_data, collections_data):
    """Sets up the Jinja2 environment with template loader and custom globals/extensions."""
    logger.info("Setting up Jinja2 environment")
    
    loader_paths = [config["templates_dir"], config["pages_dir"]]
    
    # Add all collection paths to the loader paths so Jinja2 can find collection item templates
    for collection_name, collection_settings in config.get("collections", {}).items():
        if "path" in collection_settings and os.path.exists(collection_settings["path"]):
            loader_paths.append(collection_settings["path"])

    env = Environment(loader=FileSystemLoader(loader_paths), extensions=[TagExtension])
    
    # Make site-wide data and config available under 'site' global
    env.globals.update({
        "site": {
            "config": config,
            "data": site_data,
            "collections": collections_data
        },
        # Expose url and static helpers directly for convenience in templates
        "url": lambda path: url(path, config),
        "static": lambda path: static(path, config)
    })
    return env

def _render_and_save_output(env, config, template_obj, context, output_path, source_file_path, content_for_sitemap_rss=None):
    """Internal helper to render a Jinja2 template and save it to a file."""
    try:
        output = template_obj.render(context)
    except Exception as e:
        logger.error(f"Error rendering template from '{source_file_path}' to '{output_path}': {e}")
        return None

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    logger.info("Rendered: %s -> %s", source_file_path, output_path)
    
    # Return info for sitemap/RSS
    return {
        "source_path": source_file_path,
        "output_path": output_path,
        "url": url(os.path.relpath(output_path, config["output_dir"]), config),
        "front_matter": context.get("page", {}).get("front_matter", {}),
        "content": content_for_sitemap_rss # Use the content passed for sitemap/RSS
    }

def _load_json_file_from_assets(file_path_relative_to_assets, config):
    """Helper to load a JSON file from the assets directory and return its content."""
    full_path = os.path.join(config["assets_dir"], file_path_relative_to_assets.lstrip('/'))
    if not os.path.exists(full_path):
        logger.warning(f"Page data asset file not found: {full_path}")
        return {}
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from page data asset file {full_path}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error reading page data asset file {full_path}: {e}")
        return {}


def render_all_content(config, site_data, collections_data):
    """Renders all pages and collection items."""
    env = setup_jinja_environment(config, site_data, collections_data)
    rendered_pages_info = [] # To store info for sitemap/RSS

    # Render regular pages (from pages_dir)
    logger.info("Rendering regular pages from %s", config["pages_dir"])
    for root, _, files in os.walk(config["pages_dir"]):
        for page_file in files:
            if page_file.endswith('.html'): # Only process HTML files
                page_source_path = os.path.join(root, page_file)
                output_relative_path = os.path.relpath(page_source_path, config["pages_dir"]) 
                output_path = os.path.join(config["output_dir"], output_relative_path)

                run_hook("before_render_page", page_path=page_source_path, config=config)

                with open(page_source_path, 'r', encoding='utf-8') as f:
                    full_file_content = f.read()
                front_matter, body_content_after_fm = parse_front_matter(full_file_content)

                page_data = {} # Data for server-side rendering
                data_json_urls = [] # URLs for client-side fetching

                # Load single data_file from assets
                if "data_file" in front_matter:
                    page_data = _load_json_file_from_assets(front_matter["data_file"], config)
                    # Note: url() helper now uses config['assets_dir'] internally for assets
                    data_json_urls.append(url(front_matter["data_file"], config)) 
                # Load multiple data_files from assets
                elif "data_files" in front_matter and isinstance(front_matter["data_files"], list):
                    for df_path in front_matter["data_files"]:
                        page_data.update(_load_json_file_from_assets(df_path, config)) # Merge data
                        data_json_urls.append(url(df_path, config)) # Collect all URLs

                try:
                    # For pages in 'pages_dir', the content after front matter is the template itself
                    # that extends a base layout (e.g., base.html).
                    template_obj = env.from_string(body_content_after_fm)
                except Exception as e:
                    logger.error(f"Error creating template from string for page '{page_source_path}': {e}. Ensure it has `{{% extends \"base.html\" %}}` and valid Jinja2 syntax.")
                    continue # Skip this page if template cannot be created

                context = {
                    "page": {
                        "front_matter": front_matter,
                        "data": page_data, # Make page-specific data available for server-side rendering
                        "data_json_urls": data_json_urls, # Pass URLs to the template for client-side fetching
                        "url": url(output_relative_path, config),
                        "canonical": f"{config['base_url']}/{output_relative_path.lstrip('/')}",
                        "absolute_final_url": url(output_relative_path, config)
                    },
                    "site": env.globals["site"]
                }
                
                page_info = _render_and_save_output(env, config, template_obj, context, output_path, page_source_path, content_for_sitemap_rss=body_content_after_fm)
                if page_info:
                    rendered_pages_info.append(page_info)
                run_hook("after_render_page", page_path=page_source_path, output_path=output_path, config=config)


    # Render collection items (from collections config)
    for collection_name, items in collections_data.items():
        logger.info(f"Rendering collection '{collection_name}' items.")
        for item in items:
            page_source_path = item["path"]
            
            # output_relative_path for collection items (e.g., blog/first-post.html)
            output_relative_path = os.path.join(config["collections"][collection_name]["output"], os.path.basename(page_source_path))
            output_path = os.path.join(config["output_dir"], output_relative_path)
            
            run_hook("before_render_page", page_path=page_source_path, config=config)

            layout_name = item["front_matter"].get("layout")
            if not layout_name:
                logger.warning(f"Collection item '{page_source_path}' has no 'layout' specified in front matter. Skipping.")
                continue

            # Collection items can also have page-specific data files from assets
            page_data = {}
            data_json_urls = []
            if "data_file" in item["front_matter"]:
                page_data = _load_json_file_from_assets(item["front_matter"]["data_file"], config)
                data_json_urls.append(url(item["front_matter"]["data_file"], config))
            elif "data_files" in item["front_matter"] and isinstance(item["front_matter"]["data_files"], list):
                for df_path in item["front_matter"]["data_files"]:
                    page_data.update(_load_json_file_from_assets(df_path, config))
                    data_json_urls.append(url(df_path, config))

            try:
                # For collection items, we load the specified layout template (e.g., post.html)
                template_obj = env.get_template(layout_name)
            except Exception as e:
                logger.error(f"Error loading layout template '{layout_name}' for collection item '{page_source_path}': {e}. Skipping item.")
                continue

            context = {
                "page": {
                    "front_matter": item["front_matter"],
                    "data": page_data, # Make page-specific data available for server-side rendering
                    "data_json_urls": data_json_urls, # Pass URLs to the template for client-side fetching
                    "content": item["content"], # Explicitly pass content for collection items
                    "url": url(output_relative_path, config),
                    "canonical": f"{config['base_url']}/{output_relative_path.lstrip('/')}",
                    "absolute_final_url": url(output_relative_path, config)
                },
                "site": env.globals["site"]
            }

            page_info = _render_and_save_output(env, config, template_obj, context, output_path, page_source_path, content_for_sitemap_rss=item["content"])
            if page_info:
                rendered_pages_info.append(page_info)
            run_hook("after_render_page", page_path=page_source_path, output_path=output_path, config=config)
    
    return rendered_pages_info


def copy_static(config):
    """Copies static files from 'static_dir' to the 'output_dir/static'."""
    run_hook("before_copy_static", config=config)
    logger.info("Copying static files from %s to %s", config["static_dir"], os.path.join(config["output_dir"], "static"))
    if os.path.exists(config["static_dir"]):
        shutil.copytree(config["static_dir"], os.path.join(config["output_dir"], "static"), dirs_exist_ok=True)
    else:
        logger.warning("Static directory not found: %s. Skipping static file copy.", config["static_dir"])
    run_hook("after_copy_static", config=config)

def copy_assets(config):
    """Copies assets from 'assets_dir' directly to the 'output_dir'."""
    run_hook("before_copy_assets", config=config)
    logger.info("Copying assets from %s to %s", config["assets_dir"], config["output_dir"])
    if os.path.exists(config["assets_dir"]):
        shutil.copytree(config["assets_dir"], config["output_dir"], dirs_exist_ok=True)
    else:
        logger.warning("Assets directory not found: %s. Skipping asset copy.", config["assets_dir"])
    run_hook("after_copy_assets", config=config)

def generate_sitemap(config, rendered_pages_info):
    """Generates a sitemap.xml file."""
    run_hook("before_generate_sitemap", config=config, pages=rendered_pages_info)
    logger.info("Generating sitemap.xml")
    
    urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for page in rendered_pages_info:
        loc = SubElement(urlset, 'url')
        SubElement(loc, 'loc').text = page['url']
        # Add lastmod if available (e.g., from front matter or file modification time)
        # For now, we'll just add basic URL
        
    sitemap_path = os.path.join(config["output_dir"], "sitemap.xml")
    # Pretty print XML
    rough_string = tostring(urlset, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    logger.info("Sitemap generated at: %s", sitemap_path)
    run_hook("after_generate_sitemap", config=config, sitemap_path=sitemap_path)

def generate_rss_feed(config, collections_data):
    """Generates an RSS feed (e.g., for blog posts)."""
    run_hook("before_generate_rss_feed", config=config, collections=collections_data)
    logger.info("Generating RSS feed. Looking for 'posts' collection.")

    posts = collections_data.get("posts", []) # Assuming 'posts' is a collection
    if not posts:
        logger.info("No 'posts' collection found for RSS feed generation. Skipping.")
        return

    # Sort posts by date (assuming 'date' in front matter)
    # Convert string dates to datetime objects for proper sorting
    for post in posts:
        date_str = post['front_matter'].get('date')
        if date_str and isinstance(date_str, str):
            try:
                post['front_matter']['_date_obj'] = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                logger.warning(f"Could not parse date '{date_str}' for post: {post['url']}. Using default.")
                post['front_matter']['_date_obj'] = datetime.datetime.min # Use a very old date for unparseable dates

    posts_sorted = sorted(posts, key=lambda x: x['front_matter'].get('_date_obj', datetime.datetime.min), reverse=True)
    
    rss = Element('rss', version="2.0", attrib={'xmlns:atom': 'http://www.w3.org/2005/Atom'})
    channel = SubElement(rss, 'channel')
    
    SubElement(channel, 'title').text = config.get("site_title", "My Static Site")
    SubElement(channel, 'link').text = config["base_url"]
    SubElement(channel, 'description').text = config.get("site_description", "A static site generated with Python.")
    SubElement(channel, 'lastBuildDate').text = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    atom_link = SubElement(channel, 'atom:link', href=f"{config['base_url']}/feed.xml", rel="self", type="application/rss+xml")

    # Limit to, say, 10 most recent posts
    for post in posts_sorted[:10]:
        item = SubElement(channel, 'item')
        SubElement(item, 'title').text = post['front_matter'].get('title', 'No Title')
        SubElement(item, 'link').text = post['url']
        SubElement(item, 'guid').text = post['url'] # GUID is usually the URL
        
        pub_date_obj = post['front_matter'].get('_date_obj')
        if pub_date_obj and isinstance(pub_date_obj, datetime.datetime):
            SubElement(item, 'pubDate').text = pub_date_obj.strftime("%a, %d %b %Y %H:%M:%S +0000")
        else:
            logger.warning(f"No valid date object for RSS item: {post['url']}")
        
        # Description can be a summary or a portion of the content
        description = SubElement(item, 'description')
        description.text = post['front_matter'].get('description', post['content'][:200] + "..." if len(post['content']) > 200 else post['content'])

    rss_path = os.path.join(config["output_dir"], "feed.xml")
    rough_string = tostring(rss, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(rss_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    logger.info("RSS feed generated at: %s", rss_path)
    run_hook("after_generate_rss_feed", config=config, rss_path=rss_path)


def build_command(config_path):
    """Builds the static site."""
    config = load_config(config_path)
    config["config_path"] = config_path # Store config_path for relative lookups
    
    # Initialize plugins (populates the global PLUGINS list in plugin_system.py)
    load_plugins(config) 
    run_hook("before_build", config=config)

    if os.path.exists(config["output_dir"]):
        logger.info("Clearing output directory: %s", config["output_dir"])
        shutil.rmtree(config["output_dir"])
    os.makedirs(config["output_dir"])

    site_data = load_data_files(config)
    collections_data = load_collections(config)

    rendered_pages_info = render_all_content(config, site_data, collections_data)
    copy_static(config)
    copy_assets(config) 
    generate_sitemap(config, rendered_pages_info)
    generate_rss_feed(config, collections_data)

    logger.info("Static site generation complete. Files are in %s", config["output_dir"])
    run_hook("after_build", config=config)

