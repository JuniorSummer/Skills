---
source: self-generated
name: nbs-economic-data
description: Fetch official Chinese macroeconomic data from National Bureau of Statistics (NBS/国家统计局). Access monthly economic reports, spokesperson Q&As, and data interpretations directly from stats.gov.cn.
version: 1.0.0
metadata:
  hermes:
    tags: [china, economics, macro-data, nbs, statistics, curl]
  prerequisites:
    commands: [curl, python3]
---

# NBS Official Economic Data Access

When you need Chinese macroeconomic data (GDP, CPI, PPI, retail sales, investment, industrial output, employment, trade, loans, etc.), go directly to the NBS website instead of searching engines.

## Critical Finding

**Search engines (Bing, Baidu) return generic results for Chinese economic data queries.** Go directly to the source.

## NBS Website Structure

### Data Interpretation Index
```
https://www.stats.gov.cn/sj/sjjd/
```
This page lists all recent data interpretation articles. Parse with:

```python
curl -sL 'https://www.stats.gov.cn/sj/sjjd/' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
  --connect-timeout 10 --max-time 15 | python3 -c "
import sys, re
t = sys.stdin.read()
links = re.findall(r'<a[^>]*href=[\"\'](.*?)[\"\']\s*[^>]*>(.*?)</a>', t, re.DOTALL)
for url, title in links:
    title = re.sub('<[^>]+>', '', title).strip()
    if title and ('2026' in title or '经济' in title or '运行' in title):
        print(f'{title}: {url}')
"
```

### Article URL Pattern
```
https://www.stats.gov.cn/sj/sjjd/YYYYMM/tYYYYMMDD_XXXXXXX.html
```

### Key Article Types
| Type | URL path | Content |
|------|----------|---------|
| Spokesperson Q&A | `/sj/sjjd/YYYYMM/t...` | Comprehensive monthly data across ALL indicators |
| Investment interpretation | `/sj/sjjd/YYYYMM/t...` | Detailed investment/FAI breakdown |
| Industrial interpretation | `/sj/sjjd/YYYYMM/t...` | Industrial value-added details |
| CPI/PPI interpretation | `/sj/sjjd/YYYYMM/t...` | Price data analysis |
| Housing price | `/sj/sjjd/YYYYMM/t...` | Real estate price data |

### Release Schedule
- Monthly data: ~15th-18th of following month
- Q&A published same day as data release
- Industrial profits: ~27th of following month

## Fetching Article Content

```python
import subprocess, re

url = 'https://www.stats.gov.cn/sj/sjjd/YYYYMM/tYYYYMMDD_XXXXXXX.html'
cmd = f"""curl -sL '{url}' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
  --connect-timeout 10 --max-time 15 2>/dev/null | python3 -c "
import sys,re
t = sys.stdin.read()
t = re.sub(r'<script[^>]*>.*?</script>', '', t, flags=re.DOTALL)
t = re.sub(r'<style[^>]*>.*?</style>', '', t, flags=re.DOTALL)
paras = re.findall(r'<p[^>]*>(.*?)</p>', t, re.DOTALL)
for p in paras:
    clean = re.sub('<[^>]+>', '', p).strip()
    if len(clean) > 20:
        print(clean)
        print()
" """
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
```

## Pitfalls

- **stats.gov.cn blocks direct access** to some pages (403 Forbidden) — the `/sj/sjjd/` index and article pages work, but the main data portal (`data.stats.gov.cn`) is JavaScript-rendered and cannot be fetched via curl.
- **Article IDs are not predictable** — always fetch the index page first to find the correct article URL.
- **The spokesperson Q&A** is the best single source — it covers ALL indicators (GDP, industry, retail, investment, CPI, PPI, employment, trade, services, high-tech) in one page.
- **NBS data may differ slightly** from what analysts/media report — always prefer NBS official numbers.

## Related Skills
- `curl-chinese-web-search` — for searching when you don't know the exact NBS URL
- `cn-price-data-scraping` — for specific price data sites (tzzj.cn, guojiyoujia.com)
