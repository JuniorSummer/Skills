---
name: macos-host-provisioning
description: "Use when setting up a Mac host or installing without admin."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [macOS, Provisioning, Docker, launchd, HomeServer]
    related_skills: [codex, hermes-migration]
---

# macOS Host Provisioning

Standing software up on a Mac that will host containers/services (a Mac Studio or similar
always-on box): what to check first, what genuinely needs the user at the keyboard, and how
to install the rest without admin rights.

## When to use

- "Install X on the Mac / Studio", "set up the new host", "start the DB/web/worker stack"
- Any install/startup task where the answer might be "you need admin for this"
- Wiring launchd services, remote access (Tailscale), or backups on a Mac host

Assessing hardware health / verifying a used Mac is a different job (nothing gets installed):
use `mac-hardware-verification` — and when the machine is one you cannot reach, deliver a
double-clickable report script for the user to run.

Also load the `codex` skill when delegating the mechanical parts of the install.

## Step 0 — Analysis first, written to a file (this user)

For infra/install work the user wants **no execution until a feasibility analysis exists on
disk**. Produce it before touching anything:

- Save the analysis to a file (project/workspace dir) and keep the chat reply to a short
  summary — this user reads the file, not a wall of chat.
- Every claim carries evidence you actually obtained: paste the real command output
  (hardware, ports, disk, memory, versions). Never a plausible guess.
- Structure it as **① what I can automate ② what only the user can do ③ gaps the user's own
  plan didn't cover ④ decisions still open**. The gaps section is the valuable one — an
  audited plan still tends to miss remote-login state, HTTPS/cert prerequisites, and
  whether a "reuse the existing service" credential path is even implemented.
- Verify the plan's technical assumptions against reality before agreeing (image tags and
  architectures, model names/dimensions, existing credentials). State plainly which
  assumption breaks; do not paper over it.

## Step 1 — Prechecks (one batched read-only call)

```bash
system_profiler SPHardwareDataType | grep -E "Model Name|Chip|Memory"   # model, cores, RAM
sw_vers; uname -m; df -h /
top -l 1 -n 0 | head -12; vm_stat | head -6; sysctl vm.swapusage       # RAM headroom + swap
lsof -nP -iTCP -sTCP:LISTEN | awk '{print $1, $9}' | sort -u            # who holds which port
id; sudo -n true                                                       # admin group? password-free sudo?
ls -ld /Applications /usr/local/bin ~/.local/bin                       # where can I actually write?
fdesetup status; defaults read com.apple.loginwindow autoLoginUser          # full-disk encryption + auto-login
launchctl list | grep -iE "hermes|docker|tailscale"                    # existing user agents
scutil --proxy | head -12; pgrep -lf "mihomo|clash|surge"              # egress path
```

Reading the results:

- **Ports 5000 and 7000 are held by ControlCenter (AirPlay Receiver)** on modern macOS —
  never assign 5000 to a web service; check the port before a plan commits to it.
- A local proxy/DNS client (clash/mihomo and friends) frequently occupies `*:53` and its own
  mixed port. Note it: it explains DNS surprises and it is the proxy you must point Docker
  at for registry pulls.
- Record free RAM and swap **before** sizing a container VM. A VM memory limit is a cap the
  VM grows into, so a tight host starts swapping instead of failing; size for the measured
  free number, not the plan's wish.
- `/Applications` is `drwxrwxr-x root:admin`: a member of `admin` copies an `.app` into it
  with **no sudo**. Do not assume app installs need a password.

## Step 2 — Admin boundary map

Settle early which steps need the human, since the agent must never type a password:

| Needs the user | Does NOT need the user |
|---|---|
| First launch of an app that installs a privileged helper (Docker Desktop's `DockerHelper.app`) | Downloading the dmg/zip/tarball, `hdiutil attach`, `ditto`/`cp -R` into `/Applications`, `hdiutil detach` |
| Anything writing `/usr/local/bin` (root:wheel) | Anything under `~/.local/bin`, `~/.docker`, `~/Library/LaunchAgents` |
| Enabling Remote Login (SSH) or any System Settings toggle | Creating launchd **user** agents and bootstrapping them |
| Tailscale GUI login + system-extension approval, plus enabling HTTPS certificates in the admin console | `tailscale up`, `tailscale serve` once logged in |
| Approving macOS privacy/disk permission prompts | Installing verifiable standalone binaries |

When a task hits a row on the left: prepare the exact command or step, stop, and hand that
single action to the user. Never offer to enter a password for them.

## Step 3 — User-level install recipe (no admin, checksum-verified)

Prefer single-binary tools (Go/Rust CLI releases): one `install -m 755` finishes the job.

1. Query release metadata through the proxy when the vendor is unreachable: the GitHub API
   gives the latest tag and the `darwin-arm64` asset URL.
2. Download the asset **and** the upstream checksum file. Its name varies by project
   (`SHA256SUMS`, `*_checksums.txt`, `.proof`); if there genuinely is none, record the
   sha256 you computed and label it "no upstream checksum" rather than skipping silently.
3. Verify the archive digest against the upstream line, `install -m 755` the binary into
   `~/.local/bin`, then **also** verify the installed file's sha256 against the binary
   extracted from that archive. The first comparison proves the download; only the second
   proves what you installed — an archive digest alone is not provenance.
4. Add `~/.local/bin` to PATH idempotently (the `case ":$PATH:"` idiom). Append only;
   record the file's sha256 before and diff after, so "only one line changed" is provable.
5. Verify by running the tool, not by listing it: `<tool> --version`. Exercise it once for
   real when it does something (keygen → encrypt → decrypt for an encryption tool) — a
   version string does not prove the binary works.

## Step 4 — Docker Desktop: install, wire the CLI, hand off the password step

Mount/copy/verify is fully automatable (delegate it to Codex; the mount step needs the
sandbox escalation described in that skill):

```bash
curl -L --proxy <proxy> -o downloads/Docker.dmg https://desktop.docker.com/mac/main/arm64/Docker.dmg
hdiutil attach -nobrowse -readonly downloads/Docker.dmg
ditto <volume>/Docker.app /Applications/Docker.app     # /Applications is admin-writable
hdiutil detach <volume>
```

Verify what landed, independently of whoever ran it:

```bash
defaults read /Applications/Docker.app/Contents/Info.plist CFBundleShortVersionString
codesign --verify --deep --strict --verbose=2 /Applications/Docker.app
spctl --assess --type execute -vv /Applications/Docker.app   # want: accepted, Notarized Developer ID
hdiutil info | grep -c /Volumes/Docker                       # want: 0 — no leaked mount
```

**Make the CLI work before the daemon does.** The admin prompt is only for the privileged
helper and the `/usr/local/bin` symlinks, so wire the CLI yourself, user-level:

- symlink every plugin from `/Applications/Docker.app/Contents/Resources/cli-plugins/*` into
  `~/.docker/cli-plugins/` (symlink, not copy — copies rot on app upgrade) and check for
  broken links after,
- add `/Applications/Docker.app/Contents/Resources/bin` to PATH,
- test with `docker compose version` — it answers **without a running daemon**, making it the
  correct wiring probe; `docker run` failing here is expected, not a defect.

**Do not pre-configure a registry proxy.** Docker Desktop routes pulls through its own
transparent proxy (`docker info` reports `HTTP Proxy: http.docker.internal:3128`), and pulls
succeed even where the host cannot reach `docker.com` directly. Prove it with a real
`docker pull hello-world` (a few seconds) before touching proxy settings; only if that pull
actually fails should you point Docker at the local proxy port found in Step 1.

Verifying a stack once it is up — image digest pinning without a local daemon, compose
hygiene, and the acceptance-script rules: `references/container-stack-verification.md`.

Day-2 database work on that stack — which role does what, provenance-ordered inserts,
`~/.pgpass` without leaking secrets into the transcript, and the lifecycle traps:
`references/postgres-container-operations.md`.

Then stop for the one-time first launch (privileged helper + license) — the user's only
unavoidable click, and everything container-side is blocked behind it. Say so plainly
instead of hunting for a workaround.

## Step 5 — launchd user agents on a Mac host

- **User agents start only after someone logs in.** FileVault off plus no `autoLoginUser`
  means a power-cycled host waits at the login window with every service down. Either accept
  an explicit login in the runbook or enable auto-login (state the trade-off: unencrypted
  disk plus auto-login is full access to anyone with physical access).
- Boot order matters: the stack agent polls `docker info` until it succeeds (backoff +
  timeout that logs failure) **before** `docker compose up -d`; launching compose the moment
  the app opens races the daemon.
- Plists do not inherit the login shell's PATH — use absolute paths for every binary.
- `caffeinate -s` as a `KeepAlive` agent keeps the host awake while services run, with the
  display still allowed to sleep.
- A desktop used as a host needs its own health story: an agent that writes a status file the
  runbook can check beats "it should be running".

## Step 6 — Docker Desktop settings on a host, and the data-loss trap

- **There is no `docker desktop settings` CLI** — the plugin only offers
  `start|stop|restart|diagnose|status|logs|update|enable|disable|version`. Resource limits are
  GUI-only, or edited in `~/Library/Group Containers/group.com.docker/settings-store.json`
  while Desktop is quit. Either way **verify the effect by reading it back**
  (`docker info | grep -E "CPUs|Total Memory"`), never by trusting the click.
- **Changing resources resets the VM.** Afterwards `docker images`, `docker volume ls` and
  `docker ps -a` come back empty, and a build running at that moment dies with
  `rpc error: ... EOF`. On a host holding real data this is destructive — require a verified
  backup first and tell the user plainly. With only empty structure on disk it is an
  inconvenience, which is exactly why every bring-up step must be idempotent and re-runnable.
- No `MemoryMiB`/`Cpus` key in `settings-store.json` means the user never touched resources
  and the VM sits at its default cap, which can far exceed what the host can spare. The VM
  grows on demand, so its RSS says little; size the cap from measured free RAM.
- **`AutoStart` defaults to false.** A host needs "Start Docker Desktop when you sign in"
  enabled or nothing returns after a reboot, however good the launchd agent is.
- `DockerBinInstallPath: user` means the user picked the user-level install path: expect no
  `/usr/local/bin/docker` symlinks ever, and rely on the PATH wiring from Step 4.
- Confirm the daemon and **per-container egress for the endpoints the stack will call**:
  `docker run --rm hello-world`, then
  `docker run --rm alpine:3.20 sh -c 'nslookup <api-host>; wget -q -S -O /dev/null https://<api-host>'`.
  A **`401` from `registry-1.docker.io/v2/` is success** — that endpoint answers
  unauthenticated requests that way. Do not read it as blocked egress and go chase proxy
  settings.

## Pitfalls

- Do not read "`docker` is not on PATH" as "Docker is not installed" — CLI wiring is a
  separate, user-level step from the daemon and can be done before the admin prompt.
- Do not accept an installer's success report as the state of the machine; check the artifact
  (`--version`, signature, mount residue) yourself.
- Do not size a VM/database from the plan's stated budget when measured free RAM is smaller —
  flag the conflict and start lower.
- A checksum file is not paperwork: verify the archive **and** the installed file.
- Never bypass or disable signature/notarization checks to make an install succeed; a failure
  there is stop-and-report, not a workaround.
- Backups land on a different device than the data, are encrypted, and are proven by a real
  restore — "the backup file exists" is not evidence.

## Reporting

- Deliverable is a file in the project/workspace: install report, runbook, verification
  evidence. Chat gets the summary, in this order: what is installed and verified, what is
  blocked, what the user must do next.
- Bring installer/agent scripts under version control in the project repo; keep data, `.env`,
  keys and downloaded archives out of it (`downloads/` in `.gitignore`).
