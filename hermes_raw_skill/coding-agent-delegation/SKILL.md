---
name: coding-agent-delegation
description: "Use when delegating work to a coding agent; verify results."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Delegation, Coding-Agent, Codex, Verification]
    related_skills: [macos-host-provisioning, codex]
---

# Delegating work to external coding agents

Driving a coding-agent CLI (Codex, Claude Code, OpenCode) from Hermes to produce code, config,
docs, or installer automation — and keeping the result trustworthy.
The per-CLI mechanics live in the respective skill (`codex`, `claude-code`, `opencode`); this is
the layer above them: how to run it, how to prompt it, and how to check it.

## When to use

- "Can you have Codex do this", "let Codex build/install it"
- Any bulk file generation: project skeleton, migrations, boilerplate, scripts, docs
- Installer/binary automation the user would otherwise do by hand

## Standing policy (this user)

- **Codex first, Hermes as the fallback.** Route code/config/document generation and installer
  automation to Codex by default; when it is quota-limited, killed by a timeout, or errors,
  Hermes does the same job itself. Deliverables and acceptance criteria stay identical — never
  quietly reduce scope on the fallback — and the report says which executor ran.
- Prefer Codex for mechanical breadth (many files against a fixed spec) and Hermes for the
  parts that need the conversation's context or judgment calls.

## Run mode

- **Launch anything longer than a couple of minutes with `background=true` and `notify=true`.**
  A foreground `terminal()` call has a hard timeout; when it fires, the child process is killed
  mid-task, leaving half-written files and an uncommitted repo.
- On a timeout, treat it as a handoff rather than a failure: check what actually landed
  (`git status`, list the target paths, run the tool's `--version`), finish the loose ends
  (report file, commit) yourself, and state that the run was cut off by a timeout — not by
  quota. Do not re-run the same task on spec.
- One child per coherent chunk. A run that takes 8+ minutes to generate 30 files is already too
  big to also absorb credentials setup, container starts, and end-to-end tests in the same call.

## Prompt shape

- **Every environment fact the child needs goes in the prompt**, with an instruction not to
  re-probe: proxy address and port, absolute target paths, expected byte size, ports already
  taken, the pinned image digest. Re-discovery wastes turns and invites confident wrong guesses.
- **Pin the spec, don't ask for design.** When the deliverable is many files against a fixed
  model, paste the exact table/column/enum list (or schema, or file manifest). A child asked to
  "design" a schema invents columns and fields you then have to strip.
- **State the prohibitions explicitly:** no `sudo`; no disabling or bypassing signature and
  checksum verification; no overwriting existing files (stop and report instead).
- **Scope "stop" to the prohibited step, never to the whole batch.** A brief that says "on the
  first failure, stop" is obeyed literally: one item failing (say a tool whose native driver is
  missing) makes the child abandon every remaining **independent** item and report the whole job
  as failed. Write it as: "if a step would need sudo or a verification bypass, stop that step and
  record it; otherwise record the failure and continue with the next item, then summarise per
  item" — then expect a per-item result list back.
- **Require a bounded report file** in the repo (command / exit code / key output) plus a final
  line starting `RESULT:`. Say the report must stay concise: unbounded reports balloon into
  tens of KB of pasted logs that drown the transcript and the diff.
- Ask it to **commit but not push**, then commit or amend yourself when it was cut off.
- Ask for **what it did NOT do** — the explicit gaps list is what makes the next step obvious
  instead of assumed.

## Verify the self-report

A `RESULT:` line is a self-report, not evidence. Re-derive every claim:

- files and schemas: read the artifacts; count what exists against what was asked,
- binaries: `--version`, and compare the sha256 of the installed file with the file inside the
  verified archive — an archive's own digest proves only the download,
- macOS apps: `codesign --verify --deep --strict` and `spctl --assess --type execute -vv`,
- services: run the acceptance script yourself (for the shape of one, see
  `macos-host-provisioning` → `references/container-stack-verification.md`).

Then report which parts you verified and how, instead of repeating the child's summary.

## Pitfalls

- **Sandbox limits are per-host, and they look like task failures.** On macOS a
  `workspace-write` sandbox cannot mount disk images or write `.git/index.lock`; the errors read
  like a broken installer. Escalate the sandbox for those tasks (recipe in
  `macos-host-provisioning`) and keep the scope narrow when you do.
- A child cannot enter a password, click a GUI authorization, or complete an SSO login. Plan
  those as user actions up front instead of discovering them mid-run.
- Don't read a killed run as a failed run: partial output is usually verifiable and needs only
  the last two steps finished by hand.
- Don't accept "installed successfully" for an external side effect (upload, publish, remote
  write) without reading the target back.
