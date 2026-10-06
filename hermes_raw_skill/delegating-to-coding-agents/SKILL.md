---
name: delegating-to-coding-agents
description: "Use when delegating work to a coding-agent CLI."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Delegation, Coding-Agent, Codex, Verification, Automation]
    related_skills: [codex, claude-code, opencode, dispatching-parallel-agents]
---

# Delegating work to external coding-agent CLIs

For one-shot CLI coding agents (`codex exec`, `claude`, `opencode run`) driven from a
Hermes terminal session. The per-CLI skills document flags and sandbox modes; this one
covers the brief and the loop — which is where the time actually gets lost.

## When to Use

- Any task you are about to hand to `codex exec` / `claude` / `opencode run`: build a
  feature, install a toolchain, refactor a repo, review a PR — especially when the brief
  spans more than a couple of files.
- The user asks for an install/build to be driven by an external agent, or says to fall
  back to doing it inline if that agent's quota runs out.
- Load the per-CLI skill (`codex`, `claude-code`, `opencode`) as well for its flags and
  sandbox modes; this skill governs the brief and the verification loop.

## The loop

1. Give it a git workdir first. These CLIs refuse or degrade outside a repository, and
   the workdir is the safety boundary — widen write access explicitly (e.g. `--add-dir`)
   only for directories the task genuinely needs.
2. Write the brief from `templates/agent-brief.md`. Front-load the facts it would
   otherwise rediscover: proxy address, which binaries already exist, what is writable,
   exact URLs, the verbatim error you want diagnosed. Every rediscovery costs turns and
   invites a wrong guess.
3. Launch with `background=true, notify=true` for anything beyond a couple of files.
4. Verify the effect yourself before believing anything it says.
5. Review the diff/commit; a killed run frequently has no commit at all.

## Standing rules for the brief

- **Never write "if any step fails, stop".** The agent then abandons the remaining
  *independent* subtasks too — five unrelated installs collapse into one attempt and
  nothing else happens. Say the opposite: record the failure, continue with the next
  item, report per-item results at the end.
- **Cap the report size.** Without "keep the report under N KB, include command / exit
  code / verdict per item, don't paste logs", the reply is 30 KB+ of pasted output that
  then has to be read anyway.
- **State constraints as prohibitions**, because the default posture is "make it work":
  no `sudo`, no package-manager installs, don't touch system settings, don't overwrite
  existing files (report instead).
- **Require a single machine-readable last line** (e.g. `RESULT: ...`) so the outcome is
  one line rather than a section to hunt through.
- **Say what not to do at the end**: don't start services, don't push, don't put secrets
  or generated credentials in the repo.
- **Keep each job to one repo and one purpose.** Two repos or two unrelated goals in one
  brief makes the commit trail impossible to review.

## Verifying the claim (its RESULT line is a self-report)

- Files: exist, expected size, content spot-check, and `git log` for the commit claimed.
- Binaries: `--version` actually executes — and **close the provenance chain**: hash of
  the extracted artifact equals hash of the installed file. Without that step, "checksum
  passed" only proved the archive downloaded intact, not that the installed binary came
  from it.
- macOS apps: `codesign --verify --deep --strict` plus
  `spctl --assess --type execute -vv` (expect `Notarized Developer ID`), then the version
  from `Info.plist`.
- Services: one real end-to-end call — connect and query, encrypt and decrypt, run the
  command and check its output. "Installed successfully" is not evidence.
- Then report which checks you ran. "Verified" with no command behind it is noise, and
  the user will (rightly) ask again.

## Failure modes worth recognising

- **Killed by a foreground tool timeout.** Files survive; the summary and commit do not.
  Poll the session first and inspect what landed — do not blindly re-run the same brief.
- **The sandbox blocks the operation, not the agent.** Disk-image mounting and some
  privileged writes fail under a restricted sandbox while working fine under a wider one.
  Change the sandbox mode (and the writable roots) rather than rewriting the task.
- **It stops at the first failure** even when failures are independent — usually your
  brief's fault; see the standing rules above.
- **It re-probes the environment**, sometimes reinstalling what already exists, or
  tripping over a bundled CLI that dropped out of the session PATH. Give it absolute
  paths for anything that must stay stable across a long session.

## Never delegate these

Anything needing an admin password, a GUI login, or an interactive OAuth consent. No CLI
coding agent can do them. Keep them out of the brief, forbid `sudo` in writing, and hand
the user a short numbered list of steps only they can perform — then automate everything
around them so those steps are the only thing left.
