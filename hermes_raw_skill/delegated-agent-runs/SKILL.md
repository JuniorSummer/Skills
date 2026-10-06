---
name: delegated-agent-runs
description: "Use when delegating a long job to an agent CLI."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, orchestration, background-jobs, verification]
---

# Delegating Long Jobs to External Agent CLIs

## When to Use

Handing a long, multi-file job to Codex / Claude Code / opencode and needing it to finish, to be
monitored without burning the turn, and to be verified before you report success. Use it whenever the
job will outlive a single tool call or produce artifacts you then hand to the user.

Orchestration layer only — launching, task wording, monitoring, verification. CLI flags, auth,
worktree and PR recipes live in the vendor skills (`codex`, `claude-code`, `opencode`).

## Launch

- Any job that writes more than a couple of files: `background=true, notify=true`, then do whatever
  independent work exists and **end the turn**. Completion arrives as a notification.
- If you must peek, `process_manage` `wait` **once** — it clamps to ~180 s and explicitly tells you to
  stop waiting. Do not poll in a loop, and never re-run a job the runtime auto-promoted to background
  (it is still running).
- Deliverables usually appear well before the commit does. Check the files on disk and `git log`
  before concluding a quiet-looking job failed.

## Word the task so one failure does not cascade

- Always state the execution policy: "**a single sub-item failing must not abort the task** — record
  the failure, continue with the rest, report each result." Without it, one missing optional
  dependency became four skipped deliverables.
- Give an explicit **file manifest**: every output filename plus what belongs in it. Unnamed outputs
  come back as one blob you then have to unpick.
- **Forbid fabrication**: "anything the source does not state must be written as not stated; never
  invent numbers or cite sources you have not read." Then spot-check samples against the source.
- Cap the paperwork: "keep the report under 5 KB, do not paste raw logs." Verbose reports cost
  wall-clock time and context, and delay the deliverable.
- Ask for a self-check (`node --check`, `bash -n`, run the tests) and a final `RESULT:` line.
- For Chinese-language deliverables, require braced variables (`${var}`, never a bare `$var` followed
  by a CJK character): bash under the C locale absorbs the following multibyte characters into the
  variable name and dies with an unbound-variable error.

## Verify the result yourself (mandatory)

The `RESULT:` line is a self-report, not evidence.

- Confirm the artifacts exist at the claimed paths and the commit is in `git log`.
- **Execute what was produced**: run the script, load the generated page's JS and exercise it,
  query the database, call the endpoint.
- Re-derive the claims that matter. If it says "N checks passed", find the harness and run it; if it
  says "installed", check the binary and its checksum chain.
- Then report the verified facts as yours, and explicitly name what you could **not** verify (mobile
  rendering, file-download behaviour, anything needing a physical device) rather than implying full
  coverage.

## Monitor cheaply

- Redirect the run to a log file (`> agent-run.log 2>&1`) so the transcript stays small, and read the
  tail rather than the whole log.
- Prefer several medium calls that append to a file over one giant call; progress then survives a
  timeout.

## Reporting back to the user

- Lead with the decision-relevant finding, not the process. If the artifact contains one number that
  changes the user's choice, that number goes first.
- Attach the artifacts; keep the chat message to what changed, what is verified, and what is still
  open.
