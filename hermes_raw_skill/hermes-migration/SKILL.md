---
name: hermes-migration
description: "Use when migrating a Hermes install between machines or cutting jobs over."
version: 0.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, migration, ssh, merge, config, skills, cron, backup]
    related_skills: [hermes-agent]
---

# Hermes Install Migration (machine → machine)

Moving a Hermes home (`~/.hermes`, or a profile under `~/.hermes/profiles/<name>/`) between machines — VPS↔local, VM↔host, old→new box. Full-replace is the failure mode; the deliverable is a staged **merge** that keeps the target's live setup working. The bundled `hermes-agent` skill covers day-to-day config mechanics; this skill covers migration specifically.

## When to Use
- Moving a Hermes home (`~/.hermes` or a profile) from one machine to another, either direction.
- Cloning or merging a Hermes setup's config, credentials, skills, memory, or cron onto another machine.
- Restoring a `hermes backup` into a live install where a straight overwrite (`hermes import`) would clobber a working target.
- Cutting scheduled jobs (or individual bots) over from one machine to another after a merge — pilot a subset, then full switch.

## Working agreement (this user)
- **Plan-first gate**: present the phased plan (what runs where, what needs the user's own hands) and wait for explicit confirmation. Read-only recon before the gate is fine; writes are not.
- Reports in Chinese, compact and table-first; state exactly which steps required the user (key install, approvals).
- Never print secret values anywhere — compare by key name / length / equality verdict only.
- Bulk operations can trip the command-approval layer (typical triggers: heredoc/batch script runs, writes to sensitive paths like `~/.ssh/config`): if an approval prompt times out the command is **blocked** — stop, tell the user, wait. Never retry or rephrase to route around the gate.

## Always-on rules
- **Backup both sides first.** Target: tar the key files to `~/.hermes/backups/pre-migrate-<date>/` plus pre-merge copies in staging. The source machine stays read-only unless asked.
- **Stage → compare → merge → verify → place.** Work in a workspace (`staging/`, `staging/extracted/`, `staging/pre-merge/`); keep the compare/merge scripts as files there so an interrupted run resumes instead of restarting.
- **Conflict policy**: settings → source wins; machine-specific paths, `_config_version`, and live credentials → target wins; every deviation gets printed with a revert command.
- **Skip by default** (opt-in, never silent): `state.db*`, `sessions/`, `logs/`, caches, `checkpoints/`, the `hermes-agent/` source + venv, Linux-only binaries (`bin/`), `install_id` (machine identity).
- **`hermes backup` / `hermes import` are replace, not merge** — `import` overwrites files wholesale. Fine for a full replace; for merges use this staged workflow. Re-check `--help`: the CLI evolves.
- **Config writes**: normally use `hermes config set`; a migration-scale merge is the exception — generate merged YAML with a script, assert the expected diff, place via temp file + `mv` (atomic; preserve mode 0600), then `hermes config check` + `hermes config get` smoke reads. Keep `_config_version` at the target's (newer) value; never downgrade.
- **Imported cron jobs are born paused** (recipe 7): the target ticker can fire due jobs in the gap before any later pause loop, and the source machine keeps firing its schedule → duplicate deliveries.
- **Scheduled-job cutover is its own gated phase, per job-group**: pilot a small subset → the USER confirms the messages actually arrived in the real channel → then pause SOURCE and resume TARGET (never both live). Recurring jobs can't be reactivated with `--run-now`; queue `cron run` while paused, then plain `resume` fires it as a catch-up — that is your end-to-end pipeline test. **For the full batch switch: check job-id parity across both `jobs.json`, suppress catch-up (`cron.catch_up_missed=false` + gateway restart) so resumes fast-forward missed slots instead of replaying N stale catch-ups, then verify by aggregate state (all target next-runs in the future, source active 0, no catch-up rows in `executions.db`) — never by the switch script's own stdout alone.** Recipes: `references/cron-cutover.md`.
- **Operating-policy keys are context-dependent — review them after a merge.** A headless server's `approvals.mode: manual` (or its `display.*` choices) becomes constant prompts on an interactive target; reset such keys for the target's context and report every adopted value with its revert command.

## Procedure
1. **Access.** `nc -z host 22`; key-only probe common users (`ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=8 <user>@host true` — try root, ubuntu, lighthouse). If no key works, offer in order: user runs `ssh-copy-id -i ~/.ssh/<migration_key>.pub <user>@host`; user pastes the pubkey into `authorized_keys`; password. Use a **dedicated migration key** (`-i <key> -o IdentitiesOnly=yes` on every later command). If a password is supplied anyway, use it exactly once (expect + ssh-copy-id; never echoed) to install the key, verify key-only login, then recommend rotating it afterwards.
2. **Recon (read-only).** Locate the home (`$HERMES_HOME` is often empty in non-interactive shells; check `~/.hermes`, `find /root /home /opt -maxdepth 4 -name .hermes`). Version via the install's own bin (non-interactive PATH often lacks `hermes`: try `~/.local/bin/hermes`, `~/.hermes/hermes-agent/.hermes/bin/hermes`). Running services: `systemctl list-units | grep -i hermes`, `ps aux | grep -i hermes`. Note `_config_version`, per-dir `du -sh` (sizes decide scope), `.env` key NAMES only, skills + cron inventories.
3. **Pull.** Stream a tar over ssh into staging (recipe 1); record sha256; extract. Never pull `state.db`/sessions for a config-only migration (hundreds of MB). Fetch any external stores referenced by symlinks in the same style.
4. **Compare.** Leaf-level config diff (flatten YAML to dotted paths); `.env` key-set + value-equality verdicts (never values); `auth.json` key names; skills per-file hash compare; cron summary. For each "differing files" category, sample ONE file and classify version drift vs user edit (frontmatter `version:` / `source:` helps) before choosing which side wins. Use `scripts/compare_homes.py`; save the full report.
5. **Merge.** Rules + snippets in `references/merge-recipes.md`:
   - `config.yaml`: merged = source values ∪ target-only leaves carried ∪ keep-local overrides (`_config_version`, machine paths like `terminal.cwd`, the `model` block, anything owned by `.env`). **Dry-run and assert the expected difference/carry counts BEFORE placing** — any unexpected difference is a script bug; fix it, don't rationalize.
   - `.env`: append source-only keys as a marked block; conflicting keys keep the TARGET value and get reported by name (idempotent: skip existing keys).
   - `auth.json`: keep the target's entry for providers both sides have (runtime status fields differ per machine); add source-only `credential_pool` providers.
   - `skills/`: union copy; conflicting FILES keep target and get logged; source-only dirs/files are the migration value. Handle symlinks explicitly (see pitfalls).
   - `cron/`: place `jobs.json` (pre-paused), `notepad.db`, `deliveries.db`, `executions.db`; skip `ticker_*`, `*.lock`, `output/`.
   - Straight placement: `memories/`, `scripts/`, `data/`, `pairing/`, platform dirs (`weixin/`, `whatsapp/`, …), `channel_directory.json`, `todos/`.
6. **Verify.** Comparator re-run shows only the known keep-local diff; `hermes config check`; `hermes config get model.provider|model.default|terminal.cwd`; `hermes cron list` (all paused, count matches); skills count sane; placed config sha256 == generated file.
7. **Report.** Changes table; conflicts kept local + exact revert commands (`hermes config set <k> <v>`, `hermes cron resume/remove <id>`); warnings: never run the same messaging-bot credentials on two machines at once (connection conflicts, duplicate replies); rotate any password that transited chat; offer removing the migration pubkey from the source; list skipped items as opt-in follow-ups.
8. **Cutover (only when scheduled jobs move to the target).** Localize every script job first (source absolute paths → `HERMES_HOME`/`expanduser`; source venv python → `sys.executable`; SDK imports the target lacks → stdlib equivalents; fetch companion data files and the API keys the scripts read from outside the home), then hand over pause-source → resume-target with a user-verified pilot. Checklist + mechanics: `references/cron-cutover.md`.

## Pitfalls
- **Assert VALUES, not path presence.** A get-style lookup used only to test presence returns nil for missing paths, and that nil silently becomes the carried value — a naive "all paths present" check passes. Verify each carried value against the intended source.
- **`os.walk(followlinks=False)` silently skips symlinked DIRS**, and broken absolute symlinks crash `shutil.copy2` mid-run. Enumerate links with explicit `islink` checks over both dirnames and filenames. Skill dirs often symlink to a store OUTSIDE the home (e.g. `$HOME/.agents/skills/`): fetch that store too, place it at the local equivalent, recreate the links against it.
- **macOS scripting realities**: no GNU `timeout` (rely on the calling tool's timeout); system Ruby is 2.6 (no endless `def x = ...`); `tar` is bsdtar (GNU-style `--exclude` works fine).
- **Don't assume PyYAML** in whatever Python runs your scripts — test `import yaml` first; macOS system Ruby ships Psych as a zero-install YAML parser (`ruby -ryaml -rjson`), recipe 2.
- **Tar over ssh: stdout IS the archive.** Never `echo` in the remote script; `cd <home> || exit 9` then `exec tar ...`.
- **Make every apply step idempotent** (skip-if-exists backups, key-presence checks, link-exists checks) — bulky runs get interrupted by crashes or approval timeouts, and a re-run must resume, not double-apply.
- Preserve file modes on secret files (`.env`/`auth.json` 0600) and keep a pre-merge copy before every rewrite.
- **Terminal-session exports persist across tool calls and shadow `.env` fallbacks.** A stale quoted export from earlier debugging made a working script fail — its loader used `setdefault`, so the shell value won over the file. `unset` ad-hoc exports after testing; when diagnosing env problems, check the live session env before blaming the file.
- **Normalize `export K=…` / quoted lines to plain `K=V` when moving values between dotfiles or reusing them.** A value that still carries quotes (or the `export ` prefix) is an invalid credential when passed to an API or `export`ed back.

## Support files
- `references/merge-recipes.md` — concrete recipes: pull/exclude list, YAML↔JSON without PyYAML, config-merge script core, env/auth/skills/cron snippets, verification assertions.
- `scripts/compare_homes.py` — parameterized two-home comparator (top-level, env, config, auth, skills, cron); secrets never printed.
- `references/cron-cutover.md` — scheduled-job cutover: pilot gate, delivery tests, pause/resume + catch-up mechanics, full-batch switch + catch-up suppression, two-bot split (chat stays on source / push moves to target: per-app ids, chat target discovery, delivery prerequisites), script localization sweep.
- `templates/feishu-direct-push.py` — portable no-agent cron script: stdlib Feishu send (no SDK), `.env` loader, `{"wakeAgent": false}` output.
