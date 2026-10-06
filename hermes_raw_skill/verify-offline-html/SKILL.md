---
name: verify-offline-html
description: "Use when verifying a self-contained HTML tool really works."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [verification, html, jsdom, frontend]
    prerequisites:
      commands: [node, npm]
---

# Verify an offline HTML artifact by executing it

Reading the file proves nothing. Boot it, drive it, assert the output changed.

## When to Use

- A delegated agent (Codex / Claude Code / subagent) reports it built an HTML tool,
  calculator, scorecard or dashboard and calls it "verified".
- You must confirm a *self-contained / offline* page really is self-contained, and
  prove its **computed** result (totals, weights, flags), not just its markup.
- Do not use for canvas/WebGL, real downloads or true layout checks — those need a
  real browser or a human.

## Why jsdom, not a headless browser

On this host `Google Chrome --headless=new --dump-dom file://…` **hangs** (killed at
300s even with a throwaway `--user-data-dir`). The browser tool is also unavailable
when the user's Chrome holds the real-profile lock. jsdom works and is fast.

## Setup (once per machine)

```bash
mkdir -p /tmp/domtest && cd /tmp/domtest
HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897 \
  npm install jsdom --no-audit --no-fund
```

## Static checks first

- `grep -oE '(src|href)="https?://[^"]+' tool.html` → must be **empty** for "offline/self-contained".
- Extract inline JS and syntax-check it: `node --check extracted.js`.

## Execute it

```js
const { JSDOM, VirtualConsole } = require("/tmp/domtest/node_modules/jsdom");
const errs = [];
const dom = new JSDOM(fs.readFileSync(file, "utf8"), {
  runScripts: "dangerously", pretendToBeVisual: true, url: "file://" + file,
  virtualConsole: new VirtualConsole().on("jsdomError", (e) => errs.push(e.message)),
});
```

Assert **zero** recorded errors, then count the rendered controls (buttons, selects,
rows) and read back any "live" text the page computes.

## Then simulate the user (the part that matters)

Structure being present is not the math working.

```js
const set = (el, v) => { el.value = v;
  el.dispatchEvent(new window.Event("change", { bubbles: true }));
  el.dispatchEvent(new window.Event("input",  { bubbles: true })); };
```

Score inputs are often `<select>` (options like `1 分 … 5 分`, `N/A`), not buttons —
locate them by inspecting `<option>` values, not by button text.

Set a known input, then assert the page's computed output moved as specified: totals
recomputed, coverage/percentage changed, a warning appeared. Also drive the negative
path (e.g. a veto/red-line checkbox) and confirm the warning text updates.

## Pitfall: DOM ordering assumptions

Do not assume "first half of controls = person A, second half = person B".
Interleaved (per-row column) layouts silently apply the same value to both sides and
report **zero divergence** — looking like a feature bug when it is the test's bug.
Verify grouping by reading a few neighbouring nodes first.

## Reporting

State what you executed and what changed as a result; name anything you could NOT
verify (e.g. real-browser file download, mobile rendering) instead of implying it works.
