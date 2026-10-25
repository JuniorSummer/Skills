---
name: mcp-oauth-onboarding
description: Use when an MCP server needs OAuth or returns 401.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mcp, oauth, integration, hermes]
---

# Remote MCP with OAuth

## When to use

- `POST` to an MCP endpoint returns **401** with `WWW-Authenticate: Bearer ... resource_metadata=...`
- `hermes mcp add ... --auth oauth` prints an authorize URL and then waits
- A previously working MCP server starts returning 401 (access token expired)

## Procedure

### 1. Probe the auth model

```bash
curl -sS -i -X POST "$URL" -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"hermes","version":"1"}}}'
```

Read `WWW-Authenticate` — it names the protected-resource metadata URL. That path often **includes the endpoint segment** (`<origin>/.well-known/oauth-protected-resource/mcp`); dropping it 404s.

Then fetch `<origin>/.well-known/oauth-authorization-server` for `authorization_endpoint`, `token_endpoint`, `registration_endpoint`, `scopes_supported`, and confirm `S256` in `code_challenge_methods_supported`.

### 2. Prefer Hermes's built-in OAuth

```bash
hermes mcp add <name> --url "$URL" --auth oauth
```

It registers a client, prints an authorize URL, opens the browser, then waits for a redirect-URL paste. **It may not bind the callback port**, so the browser lands on "can't connect" — the `?code=...&state=...` is still in the address bar and can be pasted back.

Prefer `--auth oauth` over a static header: Hermes stores the refresh token, so it survives the usual one-hour access-token lifetime.

### 3. Fall back to a manual OAuth when the interactive flow can't finish

1. Register a client (RFC 7591):

```bash
curl -sS -X POST "$AS/register" -H 'Content-Type: application/json' \
  -d '{"client_name":"Hermes Agent","redirect_uris":["http://127.0.0.1:8765/callback"],"grant_types":["authorization_code","refresh_token"],"response_types":["code"],"token_endpoint_auth_method":"none","scope":"<scopes>"}'
```

2. Generate PKCE: `verifier` = 48 random bytes base64url; `challenge` = base64url(sha256(verifier)). Keep `state`, and save the verifier with mode 600.
3. Start a one-shot callback server on the redirect port that writes `?code=` and `?state=` to a file and returns a "you can close this page" response.
4. Open the authorize URL with the **OS handler**, not the Hermes browser tool:

```bash
open "$AUTH_URL"     # macOS; xdg-open on Linux
```

`open` uses the user's default browser with their existing session. The Hermes browser can be unusable while Chrome holds the profile lock.

5. Exchange the code:

```bash
curl -sS -X POST "$AS/token" -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "grant_type=authorization_code&code=$CODE&redirect_uri=$REDIRECT&client_id=$CID&code_verifier=$VERIFIER"
```

6. Write the config by hand when needed:

```yaml
mcp_servers:
  <name>:
    url: "$URL"
    headers:
      Authorization: "Bearer <token>"
    timeout: 60
    connect_timeout: 30
```

### 4. Verify in two layers — connection AND data

```bash
hermes mcp list
hermes mcp test <name>      # expect "✓ Connected" + "Tools discovered: N"
```

Then **call a listing tool** (pageSize 3). An authenticated endpoint that returns zero records, zero tags, zero templates and zero user settings is almost always **the wrong account authorized** — not an empty dataset. Ask the user to re-authorize with the account that owns the data before reporting "no data".

### 5. Handle short-lived tokens

Access tokens commonly expire in one hour. Keep a refresh script that: reads the stored token file, checks expiry (`file mtime + expires_in`), POSTs `grant_type=refresh_token`, rewrites the token file (mode 600), and rewrites the `Authorization` header in `config.yaml`. Never print the token — mask it as `first6…last4`.

## Pitfalls

- **Notification responses have empty bodies.** `notifications/initialized` returns nothing; `json.loads("")` raises. Treat an empty body as a no-op.
- **Streamable HTTP may answer in SSE framing.** If the body starts with `event:` / `data:`, take the `data:` line before parsing.
- **Stateless servers send no `Mcp-Session-Id`.** Pass it only when present; don't hard-require it.
- **A second `hermes mcp add` starts a new DCR client** (new `client_id`, new `state`). A token granted to the earlier client does not carry over — finish one flow instead of interleaving two.
- **Killing a stalled `hermes mcp add` before it writes config is safe;** if it already wrote the entry, remove it explicitly when switching to the header path.
- **Tokens belong in the keychain or config, never in chat or command output you echo.** Mask them every time.
- **Re-authorizing needs a clean slate.** Delete the previous callback file and stop the old listener before generating a new URL. A leftover `?code=` file is picked up instantly by the new poller; the stale code then fails the state check and looks like an expired grant. Assert `state` equals the value saved with the PKCE verifier before exchanging.
- **Switching accounts means overwriting, not adding.** After a re-auth, replace the token file and re-sync the `Authorization` header in `config.yaml`. A stale header keeps querying the previous account — which is exactly how "the account has no data" gets reported for an account that does.
