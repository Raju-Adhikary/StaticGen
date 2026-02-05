Static Site Generator Features Overview
---------------------------------------

This static site generator is designed to be flexible and extensible, providing a solid foundation for building various types of static websites. Here's a breakdown of its core features:

### Core Build Process & Structure

1.  Configuration Loading (config.json):
    
    *   The SSG reads its operational settings from a config.json file. This includes paths for source directories, output, base URLs, site title, and collection definitions.
        
    *   **Benefit:** Centralized and easy configuration, allowing quick changes to site-wide settings.
        
2.  **Content Parsing (Front Matter):**
    
    *   Content files (pages and collection items) can include structured metadata at their beginning, enclosed by +++ delimiters. This metadata is in JSON format.
        
    *   **Benefit:** Decouples content from its presentation and allows for dynamic use of page-specific data (e.g., title, author, date, layout).
        
3.  **Template Engine (Jinja2):**
    
    *   Jinja2 is used for all templating, providing powerful features like variables, loops, conditionals, and filters.
        
    *   **Benefit:** Flexible and robust templating for dynamic content generation and consistent site design.
        
4.  Template Inheritance ({% extends %}, {% block %}):
    
    *   Allows you to define a base layout (base.html) and then extend it in child templates (pages/index.html, templates/post.html). Content is placed into named {% block %} regions.
        
    *   **Benefit:** Promotes code reuse, maintains design consistency, and simplifies site-wide layout changes.
        
5.  **Static File Copying:**
    
    *   Copies all files from the static\_dir (e.g., static/) to a static/ subdirectory within the output\_dir. This is typically for CSS, JavaScript, and images that don't need processing.
        
    *   **Benefit:** Ensures all necessary static assets are available in the built site.
        
6.  **Asset Copying:**
    
    *   Copies files from the assets\_dir directly into the root of the output\_dir. This is for assets that might be referenced directly from the root (e.g., favicon.ico, robots.txt, or specific images like detailed\_widget\_info.json).
        
    *   **Benefit:** Provides flexibility for placing assets at the root of the built site, including JSON data files for client-side fetching.
        
7.  Data Loading (\_data directory):
    
    *   Automatically loads all .json files from the data\_dir (e.g., \_data/). The data is nested according to the file structure (e.g., \_data/authors.json becomes site.data.authors).
        
    *   **Benefit:** Centralized management of global site data (e.g., author lists, social links, site settings) that can be accessed across all templates.
        
8.  **Collections Management:**
    
    *   Allows defining structured content groups (e.g., posts, products) in config.json.
        
    *   Each item in a collection is a content file with front matter and raw HTML content.
        
    *   The SSG processes these items, making their front matter and content available to a specified layout template.
        
    *   **Benefit:** Ideal for managing recurring content types like blog posts, products, or events, enabling dynamic listing and consistent rendering.
        

### Dynamic Content & Utility Features

1.  URL Generation (url tag/function):
    
    *   A custom Jinja2 tag/function ({% url 'path/to/page.html' %}) that generates correct relative or absolute URLs based on your config.json settings.
        
    *   **Benefit:** Ensures consistent and correct linking throughout your site, regardless of base URL changes or deployment environment.
        
2.  Static File URL Generation (static tag/function):
    
    *   A custom Jinja2 tag/function ({% static 'path/to/file.css' %}) that generates correct URLs for files copied from your static\_dir.
        
    *   **Benefit:** Simplifies linking to CSS, JS, and images, automatically handling the static/ subdirectory.
        
3.  Dynamic Date/Time (now tag):
    
    *   A custom Jinja2 tag ({% now "%Y-%m-%d" %}) that inserts the current date and time, formatted as specified.
        
    *   **Benefit:** Useful for displaying "last updated" dates, current year in footers, or dynamic timestamps.
        
4.  Sitemap Generation (sitemap.xml):
    
    *   Automatically generates a sitemap.xml file based on all rendered pages and collection items, aiding search engine optimization (SEO).
        
    *   **Benefit:** Helps search engines discover and crawl all pages on your site.
        
5.  \*\*RSS Feed Generation (feed.xml):
    
    *   Automatically generates an RSS 2.0 feed, specifically looking for a "posts" collection to include.
        
    *   **Benefit:** Allows users to subscribe to your blog or news updates.
        
6.  **Plugin System (Hooks):**
    
    *   Supports custom Python plugins that can hook into various stages of the build process (e.g., before/after rendering, before/after copying files).
        
    *   **Available Hooks:**
        
        *   before\_build(config)
            
        *   after\_build(config)
            
        *   before\_render\_page(page\_path, config)
            
        *   after\_render\_page(page\_path, output\_path, config)
            
        *   before\_copy\_static(config)
            
        *   after\_copy\_static(config)
            
        *   before\_copy\_assets(config)
            
        *   after\_copy\_assets(config)
            
        *   before\_generate\_sitemap(config, pages)
            
        *   after\_generate\_sitemap(config, sitemap\_path)
            
        *   before\_generate\_rss\_feed(config, collections)
            
        *   after\_generate\_rss\_feed(config, rss\_path)
            
        *   deploy(config) (Placeholder for custom deployment logic)
            
        *   create\_content(config) (Placeholder for custom content creation logic)
            
    *   **Benefit:** Highly extensible, allowing you to add custom functionality without modifying the core SSG code.
        
7.  **Development Server with Live Reloading (Watchdog):**
    
    *   Provides a local HTTP server to preview your site.
        
    *   Automatically rebuilds the site when changes are detected in source files and refreshes the browser.
        
    *   **Benefit:** Streamlines the development workflow, providing instant feedback on changes.
        
8.  **Page-Specific Data Files (from Assets):**
    
    *   Pages can specify data\_file (or data\_files as a list) in their front matter, pointing to JSON files located in the assets\_dir.
        
    *   These JSON files are copied directly to the output directory by copy\_assets.
        
    *   The SSG passes the _URLs_ to these JSON files (page.data\_json\_urls) to the template.
        
    *   Client-side JavaScript can then fetch these JSON files asynchronously, reducing initial HTML payload size.
        
    *   **Benefit:** Efficiently provides large, structured data for individual pages for client-side dynamic rendering without bloating the initial HTML response.
        

**7\. Jinja2 Cheat Sheet**
--------------------------

Jinja2 Cheat Sheet for Your Static Site Generator
-------------------------------------------------

Jinja2 is a powerful templating language used to generate dynamic content in your static site. This cheat sheet covers the most commonly used variables, tags, and filters available in your SSG's context.

### Variables (Context Data)

These are the data points accessible within your Jinja2 templates.

*   site.config:
    
    *   **Purpose:** Accesses configuration settings from config.json.
        
    *   **Example:**
        
        *   {{ site.config.site\_title }} (e.g., "My Awesome Static Blog")
            
        *   {{ site.config.base\_url }} (e.g., "http://localhost:8000")
            
        *   {{ site.config.site\_description }}
            
*   site.data:
    
    *   **Purpose:** Accesses global data loaded from JSON files in your \_data directory. The structure mirrors your file system.
        
    *   Example (if \_data/settings.json has {"contact\_email": "info@example.com"}):
        
        *   {{ site.data.settings.contact\_email }}
            
    *   Example (if \_data/authors.json has \[{"id": "john\_doe", "name": "John Doe"}\]):
        
        *   {{ site.data.authors\[0\].name }}
            
*   site.collections:
    
    *   **Purpose:** A dictionary where keys are your collection names (e.g., posts), and values are lists of dictionaries, each representing an item in that collection.
        
    *   Each item dictionary contains:
        
        *   front\_matter: The parsed front matter of the collection item.
            
        *   content: The raw HTML content of the collection item (after front matter).
            
        *   url: The relative URL to the rendered collection item.
            
        *   \_date\_obj: A Python datetime object for robust date sorting (added by SSG).
            
    *   **Example:** {% for post in site.collections.posts %}
        
*   page.front\_matter:
    
    *   **Purpose:** A dictionary containing the parsed front matter (metadata) of the _current_ page or collection item being rendered.
        
    *   **Example:**
        
        *   {{ page.front\_matter.title }}
            
        *   {{ page.front\_matter.author }}
            
        *   {{ page.front\_matter.date }}
            
        *   {{ page.front\_matter.description }}
            
*   page.content:
    
    *   **Purpose:** Holds the raw HTML content of a **collection item** (the part after the +++ front matter). It is used in layout templates (like templates/post.html) to inject the content.
        
    *   {{ page.content | safe }} {# Use | safe to prevent HTML escaping #}
        
    *   **Note:** For regular pages in pages/ that use {% extends %}, page.content is generally _not_ used for the main body, as the body content is already part of the extending template's blocks. It's still available in the page object for other purposes (like sitemap/RSS generation).
        
*   page.data:
    
    *   **Purpose:** Contains data loaded from data\_file or data\_files specified in the current page's front matter. This data is available for **server-side rendering** (i.e., directly in Jinja2).
        
    *   Example (in pages/products/widget.html after loading data\_file):
        
        *   {{ page.data.product\_name }}
            
        *   {{ page.data.specs.weight }}
            
*   page.data\_json\_urls:
    
    *   **Purpose:** A _list_ of URLs pointing to the external JSON files (from assets\_dir) specified in the page's front matter. This is primarily for **client-side JavaScript fetching**.
        
    *   {% if page.data\_json\_urls %} const fetchPromises = \[ {% for json\_url in page.data\_json\_urls %} fetch(&#x27;{{ json\_url }}&#x27;).then(response => response.json()), {% endfor %} \]; // ... Promise.all to merge data into window.pageData{% endif %}
        
*   page.url:
    
    *   **Purpose:** The relative URL of the current page or collection item in the built site.
        
    *   **Example:** /about.html, /blog/my-first-post.html
        
    *   **Usage:** [Link to this page]({{ page.url }})
        
*   page.canonical:
    
    *   **Purpose:** The absolute canonical URL of the current page or collection item, combining site.config.base\_url with the relative path. Important for SEO.
        
    *   **Usage:** 
        
*   page.absolute\_final\_url:
    
    *   **Purpose:** Provides the final, absolute URL for the current page. (Currently behaves similarly to page.url if use\_absolute\_urls is false, or the absolute URL if true).
        
    *   **Usage:** [Absolute Link]({{ page.absolute_final_url }})
        

### Tags (Control Structures & Custom Functionality)

Tags perform actions, control logic, or embed custom functionality.

*   {% extends "template\_name.html" %}:
    
    *   **Purpose:** Specifies that the current template inherits from a parent template. Must be the very first statement in a child template.
        
    *   **Example:** {% extends "base.html" %} (in pages/index.html or templates/post.html)
        
*   {% block block\_name %} ... {% endblock %}:
    
    *   **Purpose:** Defines a named block of content. Child templates can override these blocks.
        
    *   {% block title %}Default Title{% endblock %}
        
        {% block content %} {% endblock %}
        
    *   {% block title %}Home - {{ site.config.site\_title }}{% endblock %}{% block content %}
        
        Welcome!
        ========
        
        This is my home page content.
        
        {% endblock %}
        
*   {% for item in list %} ... {% endfor %}:
    
    *   **Purpose:** Loops over items in a list or iterable.
        
    *   {% for post in site.collections.posts %}
        
        ### {{ post.front\_matter.title }}
        
        {% endfor %}
        
*   {% if condition %} ... {% else %} ... {% endif %}:
    
    *   **Purpose:** Performs conditional rendering.
        
    *   {% if site.collections.posts %}
        
        We have posts!
        
        {% else %}
        
        No posts yet.
        
        {% endif %}
        
*   {% set variable = value %}:
    
    *   **Purpose:** Assigns a value to a variable within the template, useful for intermediate calculations or cleaner code.
        
    *   {% set sorted\_posts = site.collections.posts | sort(attribute='front\_matter.\_date\_obj', reverse=True) %}{% for post in sorted\_posts\[0:3\] %} {# ... #}{% endfor %}
        
*   {% static 'path/to/file.css' %} (Custom Tag):
    
    *   **Purpose:** Generates the correct URL for static files (from static\_dir).
        
    *   **Example:** 
        
*   {% url 'path/to/page.html' %} (Custom Tag):
    
    *   **Purpose:** Generates the correct URL for pages or assets in the output directory.
        
    *   **Example:** [About Us]({% url 'about.html' %})
        
*   {% now "%Y-%m-%d %H:%M:%S" %} (Custom Tag):
    
    *   **Purpose:** Inserts the current date and time, formatted using Python's strftime format codes.
        
    *   **Example:** Built on {% now "%B %d, %Y" %}
        

### Filters (Transforming Data)

Filters transform the output of a variable or expression. They are applied using the | pipe symbol.

*   | safe:
    
    *   **Purpose:** **CRITICAL:** Marks a string as "safe" for rendering, meaning Jinja2 will _not_ escape HTML characters. Use this when injecting raw HTML content (like page.content from a Markdown file or HTML content file).
        
    *   **Example:** {{ page.content | safe }}
        
*   | sort(attribute='...', reverse=True/False):
    
    *   **Purpose:** Sorts a list of dictionaries/objects. You specify the attribute to sort by. reverse=True sorts in descending order.
        
    *   **Example:** {% set sorted\_posts = site.collections.posts | sort(attribute='front\_matter.\_date\_obj', reverse=True) %}
        
    *   **Note:** For reliable date sorting, use attribute='front\_matter.\_date\_obj' as the Python backend converts the date string to a datetime object for proper comparison.
        
*   | reverse:
    
    *   **Purpose:** Reverses the order of a list.
        
    *   **Example:** {% for item in my\_list | reverse %}
        
*   \[start:end\] (Python-style Slicing):
    
    *   **Purpose:** While not strictly a filter, Jinja2 allows Python-style list slicing directly to get a subset of a list.
        
    *   **Example:** {% for post in sorted\_posts\[0:3\] %} (gets the first 3 items, indices 0, 1, 2)
        
    *   sorted\_posts\[1:\] (gets all items from the second one onwards)
        
*   | default('fallback\_value'):
    
    *   **Purpose:** Provides a default value if the variable is undefined or None.
        
    *   **Example:** {{ page.front\_matter.subtitle | default('No Subtitle') }}
        
*   | length:
    
    *   **Purpose:** Returns the number of items in a list or characters in a string.
        
    *   **Example:** Total posts: {{ site.collections.posts | length }}
        
*   | join(', '):
    
    *   **Purpose:** Joins elements of a list into a string, using the provided separator.
        
    *   **Example:** Tags: {{ page.front\_matter.tags | join(', ') }}
        
*   | tojson:
    
    *   **Purpose:** Converts a Python dictionary or list into a JSON string, suitable for embedding directly into JavaScript.
        
    *   const myData = {{ some\_python\_dict | tojson }}; console.log(myData);
        

This comprehensive set of files and documentation should get your SSG fully operational and help you build your static sites effectively!