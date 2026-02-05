
# StaticGen

StaticGen is a flexible Python-based static site generator for building static websites with templates, content collections, and clean output.

It reads your content files, applies templates using Jinja2, copies static assets, and generates a ready-to-serve site. It’s simple, extensible, and built to be clear.

## Features

- Config-driven site settings (via `config.json`)
- Content parsing with json front matter
- Easy manageable json database (`_data`)
- Jinja2 templating for layouts and pages
- Static asset copying
- Collections support (e.g., posts, products)
- Easy local build workflow

## Quick Start

1. Clone this repository  
   ```bash
   git clone https://github.com/Raju-Adhikary/StaticGen.git
   cd StaticGen
   ```

2. Create and activate a Python virtual environment

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your site
   Edit `config.json` to set paths, site title, base URL, and collections.

5. Add content
   Put your pages, posts, and data under the `pages`, `posts`, and `_data` folders.

6. Test and Build Your Site

    Build for production
   ```bash
   python -m ssg build
   ```
   
   Run a local server for testing
   ```bash
   python -m ssg serve --port 7999
   ```

7. View output
   Open the files in the `build/` folder in any browser.

## Structure

```
├── _data             # Global data (JSON files)
├── assets            # Root assets (favicon, robots, data files)
├── pages             # Standalone pages
├── posts             # Collection items (e.g., blog posts)
├── templates         # Jinja2 templates
├── static            # Static assets (css/js/images)
├── build             # Generated site output
├── config.json       # Site config
├── requirements.txt  # Python deps
└── README.md
```

## Config Example

Example entries in `config.json`:

```json

{
    "site_title": "My Awesome Static Site",
    "site_description": "A demo static site built with Python and Jinja2.",
    "base_url": "http://localhost:8000",
    "output_dir": "build",
    "pages_dir": "pages",
    "templates_dir": "templates",
    "static_dir": "static",
    "assets_dir": "assets",
    "data_dir": "_data",
    "plugins_dir": "_plugins",
    "collections": {
        "posts": {
            "path": "_posts",
            "output": "blog"
        }
    }
}


```

Adjust as needed for your project.

## License

MIT