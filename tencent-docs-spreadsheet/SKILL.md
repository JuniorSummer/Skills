---
source: self-generated
name: tencent-docs-spreadsheet
description: Read and write Tencent Docs (腾讯文档) spreadsheets. Documents the correct approach (MCP server), pitfalls of scraping attempts, and available WPS alternatives.
version: 1.0.0
metadata:
  hermes:
    tags: [tencent-docs, spreadsheet, mcp, wps, 腾讯文档]
---

# Tencent Docs Spreadsheet Access

## TL;DR

Use the `tencent-docs-mcp-server` MCP package. Do NOT attempt browser scraping — Tencent Docs renders sheet data on canvas elements, making DOM extraction impossible.

## Correct Approach: MCP Server

Package: `tencent-docs-mcp-server@1.0.0` (npm)

Configure in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  tencent-docs:
    command: "npx"
    args: ["-y", "tencent-docs-mcp-server"]
    env:
      TENCENT_DOCS_CLIENT_ID: "your_client_id"
      TENCENT_DOCS_CLIENT_SECRET: "your_client_secret"
      TENCENT_DOCS_ACCESS_TOKEN: "your_access_token"
      TENCENT_DOCS_OPEN_ID: "your_open_id"
    timeout: 30
```

Register app at: https://docs.qq.com/open/developers/

### Available MCP Tools

- `tencent_docs_get_sheet_info` — List sub-sheets (tabs) in a spreadsheet
- `tencent_docs_get_sheet_range` — Read cell data (A1 notation, max 1000 rows × 200 cols × 10000 cells)
- `tencent_docs_update_sheet_range` — Write cell data
- File/folder/doc/permission/smart-sheet operations

### File ID Format

The `file_id` for API calls uses the `globalPadId` format: `300000000$<padId>`

Extract from URL: `https://docs.qq.com/sheet/DZERRVFRvVUdxUGtJ` → padId is `DZERRVFRvVUdxUGtJ`

## Approaches That Do NOT Work

### 1. curl / HTTP requests
- Returns only shell HTML — all content loaded via JavaScript SPA
- The `opendoc` API returns metadata only, not cell data
- Cell data is delivered via WebSocket/polling, not REST API

### 2. Browser scraping (Playwright)
- Page loads but sheet content is rendered on **4 canvas elements**
- `document.body.innerText` only shows toolbar and tab names
- No DOM elements for cells (`td`, `th`, `[data-row]` all return 0)
- `window.clientVars` has metadata (tabs, maxRow, maxCol) but not cell values

### 3. Protobuf decoding
- The `opendoc` API response contains workbook data as: URL-encoded → JSON wrapper → base64 → zlib → protobuf
- Even after decoding, the protobuf format is undocumented and doesn't contain cell values in the initial response

## Playwright Notes (if needed for other tasks)

System chromium is available at `/usr/bin/chromium-browser`. Playwright's own browser is NOT installed. Use:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path='/usr/bin/chromium-browser',
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
```

## WPS Alternatives

Two npm packages for WPS integration:

| Package | Version | Use Case | Auth |
|---------|---------|----------|------|
| `wps-mcp` | 1.1.0 | WPS 多维表格 + AirScript generation | API Token + File ID + Script ID |
| `jim-wps-mcp-server` | 1.3.0 | WPS Webhook integration, search/query/images | Webhook URL + Token |

Config (commented out in hermes config, uncomment and fill credentials):

```yaml
# wps-mcp
wps:
  command: "npx"
  args: ["-y", "wps-mcp", "--apiToken", "TOKEN", "--fileId", "FILE_ID", "--scriptId", "SCRIPT_ID"]

# jim-wps-mcp-server
wps-webhook:
  command: "npx"
  args: ["-y", "jim-wps-mcp-server"]
  env:
    WPS_WEBHOOK_URL: "https://airscript.wps.cn/your-webhook-path"
    WPS_TOKEN: "your-airscript-token"
```

## Pitfalls

- Tencent Docs OpenAPI requires OAuth2 — no anonymous API access even for public documents
- The MCP SDK Python package (`pip install mcp`) must be installed for Hermes MCP support
- Canvas-rendered sheets are a common pattern in modern web spreadsheets (Google Sheets, Tencent Docs, etc.) — DOM scraping won't work
