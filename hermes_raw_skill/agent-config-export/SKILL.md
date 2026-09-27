---
name: agent-config-export
description: "Export AI agent config as a sanitized read-only package."
---

# Agent / Harness Config Export (read-only collection package)

## Purpose
Produce a self-describing, sanitized snapshot of a running agent harness's user-maintained
configuration. Used for migrating to another harness, integrating into a hub/registry, or
backup. The deliverable is a directory tree + `manifest.md` — never a description of one.

## Always-on rules
- **Read-only is a hard guarantee.** Shell-check source mtimes (`stat -c '%y %n'`) before and
after to *prove* nothing was modified. Never `mv`/`rm`/edit sources; only `copyfile` / read.
- **Secrets are redacted, never copied.** Config files containing sensitive fields get a
sanitized copy only; the raw value is replaced with `<REDACTED>` and the original value is
never written into the package NOR echoed in the reply.
- **Strict exclusion set** (do not collect): auth/credential/token/key files, cookies / Login
Data / browser profiles, SQLite/DB/WAL/shm, raw session logs / chat history / telemetry /
crash reports / caches, and complete business-project or customer data.
- **Final leak-scan is mandatory.** After building, grep the whole package for token/key patterns
and confirm zero real secrets (placeholders like `ghp_xx...xxxx`, `your-key`, `EMPTY` are fine),
zero `.db/.sqlite/.wal/.shm` files, zero cookie/profile files.
- Deliver a plain-text final report (CLI context, no markdown rendering): package absolute path,
file count + total size, excluded categories, files needing manual review, and whether any
source was modified.

## Procedure
1. **Confirm the actual harness** before copying. Inspect `~` and the running agent's config
dirs (`ls`, `find -maxdepth`) to map real paths. The environment's running harness is the
source — note its name (e.g. `hermes-agent`) into `source_harness`.
2. **Build the target tree** (mirror requested layout):
`user-rules/ project-rules/ skills/ memory/ commands/ config-sanitized/`. Preserve relative
structure inside each bucket.
3. **Classify files**: copy text/config + skill resources; exclude caches, `__pycache__`,
`node_modules`, `.git`, binaries (`.pyc/.pdf/.gz/.db/img/...`).
4. **Copy user rules / project AGENTS / skills / memory** as verbatim text copies, preserving
relative paths. For memory that lives in markdown files, copy them AND optionally emit an
`exported-memory.md` summary with per-line evidence source; NEVER copy the SQLite DB.
5. **Commands**: copy user scripts; run a literal-redaction pass on string-literal credentials
(`PASSWORD = '...'` → `<REDACTED>`). Empty hook dirs → write a small informational note.
6. **Config sanitization**: redact any `key: value` line whose key matches a sensitive-key regex
(api_key, secret, token, password, credential, access_token, channel, ...). For `.env`, redact
ALL values (secrets-only file) but keep key names + comments as a template.
7. **Emit `manifest.md`** with one row per collected file:
`source_harness / original_path / collected_path / type / scope(user|project) / purpose /
sha256 / sensitive_review(passed|needs-review) / notes`.

See `references/redaction-and-scan.md` for the regexes, exclusion lists, and side-effect notes.

## Pitfalls
- A transaction-like build (one script that copies, redacts, and writes manifest) is far more
reliable than many manual `cp` steps — write it once, run it, then audit.
- Mark redaction-touched files (`config.yaml`, `env.sanitized`, scripts with embedded creds) as
`sensitive_review: needs-review` so a human double-checks them.
- Built-in gateway hook code belongs to the app package — record only user-level hooks; if the
hooks dir is empty say so rather than copying app source.
- `.env` in Hermes is declared secrets-only by design; behavioral settings that appear to live
in `.env` should go in `config.yaml` — do not round-trip them through the export.
- Skill trees usually hold placeholders (`ghp_xx...xxxx`, `your-key`, `EMPTY`); still scan — a
real key sometimes sneaks in as an example that was never scrubbed.
