# StaticGen - Identified Limitations and Issues

This document contains a comprehensive list of limitations, issues, and improvement opportunities identified in the StaticGen project. Each issue is formatted as a GitHub issue template with proper labels and formatting.

---

## Issue 1: Missing Package Configuration (`setup.py` or `pyproject.toml`)

**Labels:** `enhancement`, `packaging`, `good first issue`

**Priority:** High

### Description
The project lacks a proper Python package configuration file (`setup.py` or `pyproject.toml`), making it difficult to install as a package and distribute via PyPI.

### Current Behavior
- Users cannot install StaticGen using `pip install staticgen`
- The package cannot be executed using `python -m ssg` (throws error: "No module named ssg.__main__")
- Requires manual setup and running via `python -c "from ssg.cli import main; main()"`

### Expected Behavior
- Users should be able to install via pip: `pip install staticgen`
- Should be executable as: `python -m ssg build` or `ssg build`
- Should be distributable on PyPI

### Proposed Solution
Add either:
1. A `setup.py` file with proper package metadata
2. A modern `pyproject.toml` file (recommended)

Include:
- Entry point for CLI: `ssg = ssg.cli:main`
- Package metadata (version, author, description, etc.)
- Dependencies from requirements.txt
- `__main__.py` file in the ssg package

### References
- [Python Packaging User Guide](https://packaging.python.org/)
- Current error: `No module named ssg.__main__; 'ssg' is a package and cannot be directly executed`

---

## Issue 2: No Automated Tests

**Labels:** `enhancement`, `testing`, `priority: high`

**Priority:** High

### Description
The project has zero test coverage, making it risky to refactor or add new features without breaking existing functionality.

### Current Behavior
- No test files exist (`test_*.py` or `*_test.py`)
- No test framework configured (pytest, unittest, etc.)
- No way to verify code changes don't break functionality
- No CI/CD to automatically run tests

### Expected Behavior
- Comprehensive test suite covering core functionality
- Unit tests for individual modules
- Integration tests for the build pipeline
- Test coverage reports

### Areas Needing Tests
1. **Front matter parsing** (`front_matter_parser.py`)
   - Valid JSON front matter
   - Invalid front matter handling
   - Edge cases

2. **Configuration loading** (`config_loader.py`)
   - Valid config files
   - Missing config files
   - Invalid JSON handling

3. **Build process** (`build_core.py`)
   - Page rendering
   - Collection rendering
   - Static file copying
   - Sitemap generation
   - RSS feed generation

4. **Plugin system** (`plugin_system.py`)
   - Plugin loading
   - Hook execution
   - Error handling

5. **URL helpers** (`url_helpers.py`)
   - URL generation
   - Base URL handling

### Proposed Solution
1. Add pytest as a dev dependency
2. Create `tests/` directory
3. Write unit tests for each module
4. Add integration tests for the full build pipeline
5. Set up pytest configuration
6. Add test coverage reporting (e.g., pytest-cov)

---

## Issue 3: No CI/CD Pipeline

**Labels:** `enhancement`, `ci/cd`, `automation`

**Priority:** High

### Description
The project lacks continuous integration and deployment pipelines, meaning there's no automated testing, building, or quality checks.

### Current Behavior
- No `.github/workflows/` directory
- No automated testing on pull requests
- No automated linting or code quality checks
- No automated releases

### Expected Behavior
- Automated tests run on every PR
- Code quality checks (linting, formatting)
- Automated builds to verify the project works
- Potential automated releases to PyPI

### Proposed Solution
Add GitHub Actions workflows:

1. **CI Workflow** (`.github/workflows/ci.yml`):
   - Run on push and PR
   - Test on multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
   - Run linters (flake8, black, isort)
   - Run tests with coverage
   - Report coverage to codecov

2. **Release Workflow** (`.github/workflows/release.yml`):
   - Trigger on version tags (e.g., v1.0.0)
   - Build package
   - Publish to PyPI
   - Create GitHub release

---

## Issue 4: Missing `__main__.py` for Module Execution

**Labels:** `bug`, `packaging`, `good first issue`

**Priority:** High

### Description
The `ssg` package cannot be executed as a module using `python -m ssg` because it lacks a `__main__.py` file.

### Current Behavior
```bash
$ python -m ssg build
/usr/bin/python: No module named ssg.__main__; 'ssg' is a package and cannot be directly executed
```

### Expected Behavior
```bash
$ python -m ssg build
INFO - Loading configuration from config.json
...
```

### Proposed Solution
Create `ssg/__main__.py` in the project root:
```python
from .cli import main

if __name__ == "__main__":
    main()
```

---

## Issue 5: No Input Validation or Error Handling for Config

**Labels:** `enhancement`, `error-handling`, `security`

**Priority:** Medium

### Description
The configuration loader (`config_loader.py`) has minimal validation, allowing invalid configurations to cause cryptic errors during build.

### Current Behavior
- No validation of required config keys
- No type checking for config values
- Missing directories cause errors later in the build process
- Invalid paths are not caught early

### Expected Behavior
- Validate all required config keys exist
- Type-check config values (strings, dicts, etc.)
- Verify directory paths exist or can be created
- Provide clear error messages for invalid configs

### Example Issues
1. Missing `output_dir` key → AttributeError later
2. Invalid `collections` structure → KeyError
3. Non-existent `templates_dir` → Jinja2 error

### Proposed Solution
Add a `validate_config(config)` function that:
- Checks for required keys
- Validates data types
- Verifies paths exist
- Returns clear error messages

---

## Issue 6: Limited Error Messages and Logging

**Labels:** `enhancement`, `usability`, `error-handling`

**Priority:** Medium

### Description
Error messages are often generic and don't provide enough context to debug issues effectively.

### Current Behavior
- Generic error messages: "Error rendering template"
- Stack traces without user-friendly explanations
- No suggestions for fixing errors
- Logging doesn't include enough debug information

### Expected Behavior
- Clear, actionable error messages
- Context about what failed and why
- Suggestions for fixing common errors
- Debug mode with verbose logging

### Examples of Needed Improvements
1. Template errors should show:
   - Which template failed
   - Which line in the template
   - What variable was undefined
   
2. File not found errors should show:
   - Full path that was attempted
   - Suggestions for fixing the path
   
3. JSON parsing errors should show:
   - Which file has invalid JSON
   - Line number of the error

### Proposed Solution
1. Add custom exception classes
2. Improve error messages with context
3. Add `--debug` flag for verbose output
4. Add `--quiet` flag for minimal output

---

## Issue 7: No Markdown Support

**Labels:** `enhancement`, `feature`, `content`

**Priority:** Medium

### Description
The project only supports HTML files for content, requiring users to write raw HTML. Most static site generators support Markdown for easier content creation.

### Current Behavior
- Only `.html` files are processed
- Users must write content in HTML
- No support for `.md` or `.markdown` files

### Expected Behavior
- Support Markdown files alongside HTML
- Convert Markdown to HTML during build
- Support common Markdown extensions (tables, code blocks, etc.)
- Allow mixing HTML and Markdown content

### Proposed Solution
1. Add `markdown` dependency (or `mistune`, `markdown-it-py`)
2. Add Markdown parser to the build pipeline
3. Process `.md` files in pages and collections
4. Convert Markdown to HTML before template rendering

### Implementation Details
- Detect file extensions (`.md`, `.markdown`, `.html`)
- Parse front matter from Markdown files
- Convert Markdown body to HTML
- Pass HTML to Jinja2 templates

---

## Issue 8: No Code Syntax Highlighting

**Labels:** `enhancement`, `feature`, `documentation`

**Priority:** Low

### Description
When Markdown support is added, there's no built-in syntax highlighting for code blocks in generated pages.

### Expected Behavior
- Code blocks should have syntax highlighting
- Support common languages (Python, JavaScript, etc.)
- Include CSS for styling code blocks

### Proposed Solution
1. Use Pygments for syntax highlighting
2. Add syntax highlighting during Markdown processing
3. Include default CSS theme or allow customization

---

## Issue 9: Hardcoded RSS Feed to 'posts' Collection

**Labels:** `enhancement`, `flexibility`

**Priority:** Low

### Description
RSS feed generation is hardcoded to only work with a collection named 'posts'. Other collections cannot generate RSS feeds.

### Current Behavior
```python
# In build_core.py line 250
posts = collections_data.get("posts", [])
```

### Expected Behavior
- Allow RSS generation for any collection
- Configure which collections should have RSS feeds in `config.json`
- Support multiple RSS feeds for different collections

### Proposed Solution
Update `config.json` to include RSS configuration:
```json
{
  "rss": {
    "enabled": true,
    "collections": ["posts", "news"],
    "output_files": {
      "posts": "blog/feed.xml",
      "news": "news/feed.xml"
    }
  }
}
```

---

## Issue 10: No Pagination Support

**Labels:** `enhancement`, `feature`

**Priority:** Medium

### Description
Collections with many items (e.g., 100+ blog posts) cannot be paginated. The index page must display all items at once.

### Current Behavior
- All collection items are passed to templates at once
- No built-in pagination mechanism
- Users must manually implement pagination in templates

### Expected Behavior
- Automatic pagination for collection listing pages
- Configurable items per page
- Previous/next page navigation
- Page number links

### Proposed Solution
Add pagination configuration:
```json
{
  "collections": {
    "posts": {
      "path": "_posts",
      "output": "blog",
      "pagination": {
        "enabled": true,
        "per_page": 10,
        "output_pattern": "blog/page/{page}/index.html"
      }
    }
  }
}
```

---

## Issue 11: No Draft Support

**Labels:** `enhancement`, `feature`, `content`

**Priority:** Low

### Description
There's no way to mark content as drafts that shouldn't be published in production builds.

### Current Behavior
- All content in collections and pages is always built
- Users must manually move draft files out of directories

### Expected Behavior
- Support `draft: true` in front matter
- Drafts are excluded from production builds
- Drafts can be included in development builds with a flag

### Proposed Solution
1. Add draft support in front matter:
   ```json
   {
     "title": "My Draft Post",
     "draft": true
   }
   ```

2. Add `--include-drafts` flag to build command

3. Skip draft items unless flag is set

---

## Issue 12: No Asset Optimization

**Labels:** `enhancement`, `performance`

**Priority:** Low

### Description
Static assets (CSS, JS, images) are copied as-is without any optimization, leading to larger file sizes and slower page loads.

### Current Behavior
- Files are copied directly without processing
- No minification of CSS/JS
- No image optimization
- No asset fingerprinting for cache busting

### Expected Behavior
- Minify CSS and JavaScript files
- Optimize images (compress, resize)
- Add content hashes to filenames for cache busting
- Generate multiple image sizes for responsive images

### Proposed Solution
1. Add optional asset pipeline
2. Integrate with tools like:
   - cssmin/rcssmin for CSS
   - jsmin/uglify for JavaScript
   - Pillow for image optimization
3. Make optimization opt-in via config

---

## Issue 13: No Template Caching

**Labels:** `enhancement`, `performance`

**Priority:** Low

### Description
Jinja2 templates are not cached, potentially slowing down builds with many pages.

### Current Behavior
- Templates are loaded fresh on every render
- No bytecode caching enabled

### Expected Behavior
- Enable Jinja2 bytecode cache
- Faster subsequent builds

### Proposed Solution
Enable Jinja2's bytecode cache:
```python
from jinja2 import FileSystemBytecodeCache
env = Environment(
    loader=FileSystemLoader(loader_paths),
    bytecode_cache=FileSystemBytecodeCache(cache_dir)
)
```

---

## Issue 14: No Built-in Search Functionality

**Labels:** `enhancement`, `feature`

**Priority:** Low

### Description
No support for site search functionality, requiring users to integrate third-party solutions.

### Expected Behavior
- Generate search index during build
- Provide client-side search (lunr.js, pagefind)
- Or static search results pages

### Proposed Solution
Add optional search index generation:
1. Generate JSON index of all pages
2. Include page titles, content, URLs
3. Optional: Include lunr.js integration

---

## Issue 15: Limited Documentation

**Labels:** `documentation`, `good first issue`

**Priority:** Medium

### Description
While GUIDE.md exists, the project lacks comprehensive documentation for advanced features and API reference.

### Missing Documentation
1. **API Documentation**
   - Module-level docstrings
   - Function/class documentation
   - Type hints

2. **Advanced Guides**
   - Creating custom plugins
   - Extending Jinja2 with custom filters
   - Advanced configuration examples
   - Theming guide

3. **Troubleshooting Guide**
   - Common errors and solutions
   - Performance optimization tips
   - Debugging techniques

4. **Examples Directory**
   - Example themes
   - Example plugins
   - Different site types (blog, docs, portfolio)

### Proposed Solution
1. Add docstrings to all modules and functions
2. Generate API docs using Sphinx or mkdocs
3. Create comprehensive tutorials
4. Add examples directory with working examples

---

## Issue 16: No Version Management

**Labels:** `enhancement`, `project-management`

**Priority:** Medium

### Description
The project has no version number or version management strategy.

### Current Behavior
- No `__version__` in the package
- No version in config or output
- No way to track which version built a site

### Expected Behavior
- Version number in `ssg/__init__.py`
- Version shown in CLI (`ssg --version`)
- Version written to generated sites (meta tag or comment)

### Proposed Solution
1. Add version to `ssg/__init__.py`:
   ```python
   __version__ = "0.1.0"
   ```

2. Add `--version` flag to CLI

3. Follow semantic versioning

---

## Issue 17: Placeholder Commands Not Implemented

**Labels:** `enhancement`, `feature`

**Priority:** Low

### Description
Two CLI commands are placeholders and don't actually do anything: `deploy` and `create`.

### Current Behavior
```python
# In cli.py
def deploy_command(config_path):
    logger.info("Deploy command is a placeholder...")
    
def create_command(config_path):
    logger.info("Create command is a placeholder...")
```

### Expected Behavior
**Deploy Command:**
- Deploy to various platforms (Netlify, GitHub Pages, Vercel)
- Support FTP/SFTP deployment
- Integration with hosting providers

**Create Command:**
- Create new pages: `ssg create page about`
- Create new posts: `ssg create post "My First Post"`
- Create new collections: `ssg create collection products`

### Proposed Solution
1. Implement basic `create` command first (higher priority)
2. Add deploy command with plugin system support
3. Document deployment workflows in README

---

## Issue 18: No Configuration Validation Schema

**Labels:** `enhancement`, `developer-experience`

**Priority:** Low

### Description
No JSON schema or validation for the configuration file, making it hard for users to know what's valid.

### Expected Behavior
- JSON schema file for `config.json`
- IDE autocompletion for config
- Validation errors with helpful messages

### Proposed Solution
1. Create `config-schema.json`
2. Add schema validation using `jsonschema` library
3. Reference schema in config files

---

## Issue 19: No Watch Mode Debouncing Improvement

**Labels:** `enhancement`, `developer-experience`

**Priority:** Low

### Description
The file watcher has a basic 1-second debounce, but it rebuilds the entire site on every change, which can be slow for large sites.

### Current Behavior
- Full site rebuild on any file change
- 1-second debounce
- Can be slow for large sites

### Expected Behavior
- Incremental builds (only rebuild changed pages)
- Smarter debouncing
- Show what changed and what was rebuilt

### Proposed Solution
1. Implement incremental build logic
2. Track file dependencies
3. Only rebuild affected pages
4. Show clear output about what changed

---

## Issue 20: Missing Security Headers in Dev Server

**Labels:** `security`, `developer-experience`

**Priority:** Low

### Description
The development server doesn't set any security headers, which could mask issues that would appear in production.

### Expected Behavior
- Set common security headers
- Option to simulate production headers
- Help developers catch security issues early

### Proposed Solution
Add security headers to dev server:
- Content-Security-Policy
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection (legacy browsers)

---

## Issue 21: No Plugin Documentation or Examples

**Labels:** `documentation`, `plugins`

**Priority:** Medium

### Description
The plugin system exists but has no documentation or example plugins, making it hard for users to extend functionality.

### Current Behavior
- Plugin system works
- No example plugins
- No documentation on available hooks
- No guide on writing plugins

### Expected Behavior
- Clear documentation of all hooks
- Example plugins in `_plugins/` or `examples/plugins/`
- Guide on writing custom plugins

### Available Hooks (Need Documentation)
- `before_build`
- `after_build`
- `before_render_page`
- `after_render_page`
- `before_copy_static`
- `after_copy_static`
- `before_copy_assets`
- `after_copy_assets`
- `before_generate_sitemap`
- `after_generate_sitemap`
- `before_generate_rss_feed`
- `after_generate_rss_feed`
- `deploy`
- `create_content`

### Proposed Solution
1. Create `PLUGINS.md` documentation
2. Add example plugins:
   - Image optimizer plugin
   - SEO validator plugin
   - Link checker plugin
   - Analytics injection plugin

---

## Issue 22: No Type Hints

**Labels:** `enhancement`, `code-quality`

**Priority:** Low

### Description
The codebase lacks type hints, making it harder to catch bugs and reducing IDE support.

### Current Behavior
- No type hints on functions
- No mypy or type checking

### Expected Behavior
- Type hints on all function signatures
- Return type annotations
- mypy type checking in CI

### Proposed Solution
1. Add type hints gradually to all modules
2. Add mypy to dev dependencies
3. Configure mypy in `setup.cfg` or `pyproject.toml`
4. Add mypy to CI pipeline

---

## Issue 23: No Incremental Build Support

**Labels:** `enhancement`, `performance`

**Priority:** Low

### Description
Every build clears and rebuilds the entire site, even if only one file changed. For large sites, this is inefficient.

### Current Behavior
```python
# In build_core.py line 316
if os.path.exists(config["output_dir"]):
    shutil.rmtree(config["output_dir"])  # Deletes everything
```

### Expected Behavior
- Track file modifications
- Only rebuild changed pages
- Only copy changed assets
- Dramatically faster builds for large sites

### Proposed Solution
1. Add build cache/metadata
2. Track file modification times
3. Implement smart rebuild logic
4. Add `--clean` flag to force full rebuild

---

## Issue 24: Missing robots.txt Generation

**Labels:** `enhancement`, `seo`

**Priority:** Low

### Description
No automatic `robots.txt` generation, requiring users to manually create it in assets.

### Expected Behavior
- Auto-generate `robots.txt` based on config
- Include sitemap reference
- Allow customization

### Proposed Solution
Add to config:
```json
{
  "robots": {
    "enabled": true,
    "allow": ["/"],
    "disallow": ["/admin/", "/private/"],
    "sitemap": true
  }
}
```

---

## Issue 25: No Image Lazy Loading Support

**Labels:** `enhancement`, `performance`

**Priority:** Low

### Description
No built-in support for modern image best practices like lazy loading, responsive images, or WebP conversion.

### Expected Behavior
- Automatically add `loading="lazy"` to images
- Generate srcset for responsive images
- Optional WebP conversion

### Proposed Solution
Add image processing plugin or built-in feature:
1. Parse HTML for img tags
2. Add lazy loading attributes
3. Generate multiple sizes
4. Add srcset attributes

---

## Summary

This document identifies **25 limitations and issues** in the StaticGen project, categorized as follows:

### By Priority
- **High Priority**: 4 issues (packaging, testing, CI/CD, module execution)
- **Medium Priority**: 6 issues (error handling, docs, pagination, etc.)
- **Low Priority**: 15 issues (nice-to-have features and optimizations)

### By Category
- **Packaging & Installation**: 3 issues
- **Testing & Quality**: 3 issues
- **Documentation**: 3 issues
- **Features**: 10 issues
- **Performance**: 4 issues
- **Security**: 1 issue
- **Developer Experience**: 4 issues

### Recommended Implementation Order
1. **Phase 1 - Foundation** (High Priority)
   - Issue #1: Package configuration
   - Issue #4: `__main__.py` file
   - Issue #2: Automated tests
   - Issue #3: CI/CD pipeline

2. **Phase 2 - Core Improvements** (Medium Priority)
   - Issue #5: Config validation
   - Issue #6: Better error messages
   - Issue #15: Documentation improvements
   - Issue #16: Version management

3. **Phase 3 - Feature Expansion** (Selected Low Priority)
   - Issue #7: Markdown support
   - Issue #10: Pagination
   - Issue #17: Implement placeholder commands
   - Issue #21: Plugin documentation

4. **Phase 4 - Optimization** (Remaining Low Priority)
   - Performance improvements
   - Asset optimization
   - Additional features

---

## How to Use This Document

Each issue above can be copied and pasted directly into GitHub Issues. The recommended approach:

1. Create labels in GitHub: `enhancement`, `bug`, `documentation`, `testing`, `ci/cd`, `security`, `performance`, `good first issue`, `priority: high`, `priority: medium`, `priority: low`

2. Create issues for Phase 1 items immediately

3. Create issues for Phase 2 and 3 based on project priorities and community feedback

4. Add milestones for different phases

5. Use projects board to track progress

---

*This document was generated through code analysis and represents potential improvements to make StaticGen more robust, user-friendly, and feature-complete.*
