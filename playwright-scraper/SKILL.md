---
name: playwright-scraper
description: Use Playwright to scrape dynamic web pages with JavaScript rendering support. Ideal for scraping SPAs, infinite-scroll feeds, lazy-loaded content, and sites requiring authentication or interaction.
version: 1.0.0
author: waisimon (via ClawHub mirror)
metadata:
  hermes:
    tags: [playwright, scraper, web-scraping, automation, browser]
    homepage: https://github.com/waisimon/playwright-scraper-skill
  prerequisites:
    commands: [playwright, python3]
    packages: [playwright, requests]
  examples:
    - Scrape a dynamic single-page application
    - Extract data from infinite-scroll social feeds
    - Login and scrape authenticated content
    - Handle CAPTCHA-challenged pages
---

# Playwright Scraper Skill

This skill provides web scraping capabilities using Playwright, a powerful browser automation tool. Unlike simple HTTP requests, Playwright can execute JavaScript, wait for dynamic content, and interact with web pages.

## Quick Start

```python
from playwright.sync_api import sync_playwright
import json

def scrape_page(url: str, selector: str = None) -> dict:
    """Scrape a URL and optionally extract specific elements."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        
        if selector:
            data = page.evaluate(f"""
                () => {{
                    const elements = document.querySelectorAll('{selector}');
                    return Array.from(elements).map(el => {{
                        return {{
                            text: el.innerText?.trim(),
                            href: el.href,
                            html: el.innerHTML?.trim().substring(0, 200)
                        }};
                    }});
                }}
            """)
        else:
            data = {"html": page.content(), "title": page.title()}
        
        browser.close()
        return data

# Example usage
result = scrape_page("https://example.com", "article h2")
print(json.dumps(result, indent=2))
```

## Core Functions

### 1. Basic Page Scraping

```python
from playwright.sync_api import sync_playwright

def basic_scrape(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        result = {
            "title": page.title(),
            "url": page.url,
            "content": page.content()[:5000]
        }
        
        browser.close()
        return result
```

### 2. Wait for Dynamic Content

```python
def wait_for_content(url: str, wait_selector: str, timeout: int = 30000) -> dict:
    """Wait for specific content to load."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until="networkidle")
            page.wait_for_selector(wait_selector, timeout=timeout)
            
            result = {
                "found": True,
                "text": page.locator(wait_selector).first.inner_text()
            }
        except Exception as e:
            result = {"found": False, "error": str(e)}
        
        browser.close()
        return result
```

### 3. Handle Infinite Scroll

```python
def scroll_and_scrape(url: str, item_selector: str, max_scrolls: int = 5) -> list:
    """Scroll down to load more content."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        items = []
        for _ in range(max_scrolls):
            # Scroll to bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)  # Wait for new content
            
            # Extract items
            new_items = page.locator(item_selector).all_inner_texts()
            items.extend(new_items)
        
        browser.close()
        return list(set(items))  # Deduplicate
```

### 4. Login and Authenticated Scraping

```python
def login_and_scrape(url: str, login_url: str, credentials: dict) -> dict:
    """Login to a site and scrape authenticated content."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to login
        page.goto(login_url)
        page.fill("#username", credentials["username"])
        page.fill("#password", credentials["password"])
        page.click("#login-button")
        page.wait_for_url("**/dashboard/**", timeout=10000)
        
        # Navigate to target URL
        page.goto(url)
        content = page.content()
        
        browser.close()
        return {"success": True, "content_length": len(content)}
```

### 5. Take Screenshot

```python
def capture_screenshot(url: str, output_path: str, full_page: bool = False) -> str:
    """Capture a screenshot of a webpage."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        page.goto(url, wait_until="networkidle")
        page.screenshot(path=output_path, full_page=full_page)
        
        browser.close()
        return output_path
```

### 6. Extract Table Data

```python
def extract_table(url: str, table_selector: str = "table") -> list[dict]:
    """Extract data from an HTML table."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # Get headers
        headers = page.locator(f"{table_selector} th").all_inner_texts()
        
        # Get all rows
        rows = page.locator(f"{table_selector} tr").all()
        data = []
        
        for row in rows[1:]:  # Skip header row
            cells = row.locator("td").all_inner_texts()
            if cells:
                data.append(dict(zip(headers, cells)))
        
        browser.close()
        return data
```

## Common Use Cases

### Scraping JavaScript-Rendered Content

Many modern sites use React, Vue, Angular, or other JS frameworks. Traditional HTTP requests won't work:

```python
# This won't work for JS-rendered sites
import requests
response = requests.get(url)
# Response won't contain the actual content

# Use Playwright instead
from playwright.sync_api import sync_playwright

def scrape_spa(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        
        # Wait for React/Vue to mount
        page.wait_for_timeout(2000)
        content = page.content()
        
        browser.close()
        return content
```

### Handling Lazy-Loaded Images

```python
def scrape_lazy_loaded(url: str, img_selector: str = "img.lazy") -> list[str]:
    """Extract URLs from lazy-loaded images."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # Scroll to trigger lazy loading
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 1000)")
            page.wait_for_timeout(1000)
        
        # Get all image sources
        srcs = page.locator(img_selector).evaluate_all(
            "els => els.map(e => e.src)"
        )
        
        browser.close()
        return srcs
```

### Handling Cookies and Sessions

```python
def scrape_with_cookies(url: str, cookies: list[dict]) -> str:
    """Use pre-defined cookies to access protected content."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Set cookies
        context = browser.new_context()
        context.add_cookies(cookies)
        
        page.goto(url)
        content = page.content()
        
        browser.close()
        return content
```

## Installation

### Install Playwright

```bash
# Install Playwright Python package
pip install playwright

# Install browser binaries
playwright install chromium
# or install all browsers
playwright install
```

### Install Dependencies

```bash
# For Ubuntu/Debian
sudo apt-get install -y libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

# For macOS
brew install playwright
playwright install-deps
```

## Tips and Best Practices

1. **Headless vs Headed**: Use `headless=True` for production, `headless=False` for debugging
2. **Wait Strategies**: Prefer `wait_for_selector()` over `wait_for_timeout()`
3. **Rate Limiting**: Add delays between requests to avoid being blocked
4. **User-Agent**: Set a realistic user agent to avoid detection
5. **Incognito Context**: Use new context for isolated sessions
6. **Viewport**: Set appropriate viewport size for responsive sites

```python
# Complete example with best practices
from playwright.sync_api import sync_playwright

def robust_scrape(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.new_page()
        
        # Set extra HTTP headers
        page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9'
        })
        
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)  # Let JS execute
        
        result = {
            "title": page.title(),
            "url": page.url,
            "html": page.content()
        }
        
        browser.close()
        return result
```

## Troubleshooting

### Page doesn't load
- Check if the URL is correct
- Increase timeout
- Try with `headless=False` to see what's happening

### Content not found
- The page might be a SPA - wait longer or use `wait_until="networkidle"`
- The selector might be wrong - inspect the page first

### Blocked by CAPTCHA
- Consider using proxy rotation
- Slow down scraping speed
- Some sites require special handling

### Memory issues
- Reuse browser context when possible
- Call `browser.close()` in finally block
- Consider using browser_pool for large-scale scraping