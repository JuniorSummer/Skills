---
source: self-generated
name: curl-chinese-web-search
description: Use curl to search Chinese content via search engines (Bing, DuckDuckGo). Handles URL encoding of Chinese characters, HTML parsing, and article fetching. Use when web_search/browser tools are unavailable or timing out, and you need to search for Chinese-language content.
version: 1.0.0
metadata:
  hermes:
    tags: [curl, search, chinese, web-scraping, url-encoding]
  prerequisites:
    commands: [curl, python3]
---

# Chinese Web Search via Curl

When browser tools time out and web_search is unavailable, use curl + Bing to search Chinese content.

## Critical Pitfall: URL Encoding

**Chinese characters MUST be percent-encoded in curl URLs.** Raw Chinese in URL returns 0 bytes.

```python
# ❌ WRONG - returns empty response
curl 'https://cn.bing.com/search?q=2026年汽车以旧换新'

# ✅ CORRECT - URL-encode the query first
import urllib.parse
q = urllib.parse.quote('2026年汽车以旧换新')
# Then: curl f'https://cn.bing.com/search?q={q}'
```

## Complete Working Pattern

```python
from hermes_tools import terminal
import urllib.parse

query = '你的中文搜索词'
encoded = urllib.parse.quote(query)

result = terminal(f"""curl -sL 'https://cn.bing.com/search?q={encoded}' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  --connect-timeout 10 --max-time 15 2>/dev/null | python3 -c "
import sys,re
t = sys.stdin.read()
results = re.findall(r'<li class=\\\"b_algo\\\"[^>]*>(.*?)</li>', t, re.DOTALL)
for i, r in enumerate(results[:8]):
    title = re.search(r'<h2[^>]*>(.*?)</h2>', r, re.DOTALL)
    title = re.sub('<[^>]+>', '', title.group(1)).strip() if title else ''
    snippet = re.search(r'<p[^>]*>(.*?)</p>', r, re.DOTALL)
    snippet = re.sub('<[^>]+>', '', snippet.group(1)).strip() if snippet else ''
    url = re.search(r'href=\\\"(https?://[^\\\"]+)\\\"', r)
    url = url.group(1) if url else ''
    print(f'{i+1}. {title}')
    print(f'   {snippet[:300]}')
    print(f'   {url}')
    print()
" 2>/dev/null""", timeout=20)
```

## Fetching Article Content

After finding URLs from search results, fetch full articles:

```python
result = terminal(f"""curl -sL '{article_url}' \
  -H 'User-Agent: Mozilla/5.0' --connect-timeout 10 --max-time 15 2>/dev/null | python3 -c "
import sys,re
t = sys.stdin.read()
t = re.sub(r'<script[^>]*>.*?</script>', '', t, flags=re.DOTALL)
t = re.sub(r'<style[^>]*>.*?</style>', '', t, flags=re.DOTALL)
paras = re.findall(r'<p[^>]*>(.*?)</p>', t, re.DOTALL)
for p in paras:
    clean = re.sub('<[^>]+>', '', p).strip()
    if len(clean) > 10:
        print(clean)
        print()
" 2>/dev/null""", timeout=20)
```

## Search Engine Notes

| Engine | Chinese Query Support | HTML Parsing |
|--------|----------------------|--------------|
| **Bing (cn.bing.com)** | ✅ Best for Chinese | `<li class="b_algo">` blocks |
| **DuckDuckGo HTML** | ⚠️ Often blocked | `class="result__snippet"` |
| **Google** | ❌ Heavy JS, times out | Not parseable via curl |
| **Baidu** | ⚠️ Anti-bot, JS-heavy | Not reliable via curl |

## Troubleshooting

- **0 bytes returned**: Query not URL-encoded. Use `urllib.parse.quote()`
- **CAPTCHA/redirect**: Add realistic User-Agent and Accept-Language headers
- **Empty parsing results**: Check `len(t)` first to confirm content received
- **Timeout**: Use `--connect-timeout 10 --max-time 15` to fail fast
