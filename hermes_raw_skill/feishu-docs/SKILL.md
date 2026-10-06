---
name: feishu-docs
description: "Use when the user links a Feishu doc or 智能纪要."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [feishu, lark, docx, openapi, meeting-notes]
  prerequisites:
    commands: [curl, python3]
---

# Reading Feishu (Lark) Documents

## When to Use

The user pastes a Feishu link — `…/docx/<token>`, a wiki page, or a shared 智能纪要 — with or without
a share password, and wants it read, quoted, summarized, or turned into an analysis of its decisions
and numbers. Also use it when the link does not open in the browser but the content is needed.

The bot app's own credentials can read the document directly through the OpenAPI — **do this before
asking for a screenshot, an export, or the original audio.**

## Credentials

`FEISHU_APP_ID` / `FEISHU_APP_SECRET` live in the active profile's `.env`. `read_file` refuses that
file (secret-bearing, by design), so load it inside the shell — values never enter the transcript:

```bash
cd ~/.hermes/profiles/<profile>
set -a; source .env 2>/dev/null; set +a
```

The document id is the path segment after `/docx/`. A share-link password is irrelevant on the API
path once the app has been granted access to the document — never ask the user to remove it.

## Procedure

1. **Tenant token** — `POST /open-apis/auth/v3/tenant_access_token/internal` with
   `{"app_id":…,"app_secret":…}` → `tenant_access_token`. Send it as `Authorization: Bearer <token>`
   on every later call.
2. **Metadata** — `GET /open-apis/docx/v1/documents/{doc_id}` → title, revision.
3. **Full text** — `GET /open-apis/docx/v1/documents/{doc_id}/raw_content` returns the whole document
   as plain text. **Write it to a file; do not print it** (a long doc floods context).
4. **Blocks** (only if you need images/files/structure) —
   `GET /open-apis/docx/v1/documents/{doc_id}/blocks?page_size=500`, loop while `has_more` with
   `page_token`. Useful block types: `27` image, `43` board, `31` table, `12` text.
5. Work from the saved file with `search_files` (scan for the numbers you care about) and `read_file`
   (page through it), and quote 原句 rather than paraphrasing numbers.

## Read the tail, not just the summary (the expensive mistake)

A 智能纪要 is laid out as **标题 → 总结 (themed paragraphs) → 章节时间轴 (timestamped chapters) →
关键决策 → 金句时刻**. The summary reads well but the **hard numbers** — spending minimums, per-table
prices, date thresholds, deposit percentages — often appear *only* in the later sections. One pass
that stopped at the summary missed the entire booking-threshold and deposit dataset that sat in
关键决策 and the transcript chapters. **Load the file completely, then scan it with `search_files`
for 元 / 低消 / 门槛 / 定金 / 日期 before concluding something is not there.**

These documents also contradict themselves: a hall named in the summary may be named differently in
关键决策. Treat any mismatch as an open question for the user to confirm on site, and say so.

## When a scope is missing

The app may hold document-read but not media/export scopes. The API answers `400` with body
`{"code":99991672, "msg":"Access denied. One of the following scopes is required: […]", …}` and
**includes a ready-made grant URL** (`https://open.feishu.cn/app/<app_id>/auth?q=<scopes>…`).

- `raw_content` and `blocks` need only docx read scope and normally work.
- Image download (`GET /open-apis/drive/v1/medias/{file_token}/download`) and PDF export
  (`POST /open-apis/drive/v1/export_tasks` → poll `export_tasks/{ticket}` → download
  `export_tasks/file/{file_token}/download`) need extra scopes. For docx images the media call also
  requires `?extra={"drive_route_token":"<doc_id>"}` (URL-encoded).
- **Do not re-architect around a missing scope.** Report the exact missing scope, offer the one-click
  grant URL, and note that a tenant app may need a version release before new scopes take effect —
  then offer the cheap alternative: **the user screenshots the few images** and you read them with
  vision/OCR (`tesseract img.png stdout -l chi_sim+eng --psm 6`; upscaling 2–3× first helps Chinese).
- Cheap diagnostics beat guessing: print the raw error body (`e.read()` on `HTTPError`) — the message
  carries both the missing scope list and the grant link.

## Working notes

- Prefer `python3` + `urllib` in a script file over a long `curl | python -c` one-liner: the token
  flow plus pagination is multi-step, and re-running a script is cheaper than rebuilding a pipeline.
- Keep paging loops bounded and print only counts, not bodies.
- Numbers from a meeting summary are **what the salesperson said**, not verified facts: label them as
  quoted, mark anything absent as not stated, and carry them into the on-site verification list.
