# Siteimprove MCP

An unofficial MCP server for the [Siteimprove REST API](https://api.siteimprove.com/v2/documentation), exposing ~530 tools. This is not an official Siteimprove product.

A hosted instance is available — see [Connect to Claude.ai](#connect-to-claudeai) below.

To self-host, follow the setup steps.

## Architecture

| File | Purpose |
|---|---|
| `src/framework.ts` | Generic OpenAPI → MCP factory (reusable for any OpenAPI-backed API) |
| `src/toToolName.ts` | Siteimprove-specific tool name encoding (abbreviations + djb2 hash for long names) |
| `src/index.ts` | Wires the two above together with Siteimprove's spec URL, credential check, and login page |
| `wrangler.toml` | Cloudflare Workers config: Worker name, KV binding for OAuth sessions |

## Prerequisites

- **Node.js 18+** and **npm**
- **Cloudflare account** (free tier is fine) — [sign up](https://dash.cloudflare.com/sign-up)
- **Wrangler CLI** — install globally or use `npx wrangler` throughout:
  ```bash
  npm install -g wrangler
  ```
- **Siteimprove account** with API access — get your API key under **Profile → API Access** in the Siteimprove UI

## First-time setup

### 1. Install dependencies

```bash
cd demos/siteimprove-mcp
npm install
```

### 2. Log in to Cloudflare

```bash
wrangler login
```

This opens a browser to authenticate. Your credentials are saved locally.

### 3. KV namespace for OAuth sessions

The Worker stores OAuth tokens in a Cloudflare KV namespace. The `wrangler.toml` points at an existing KV namespace ID (`c998596807ad49f99fe5cc9b8ee23909`) — this is just an identifier, not a secret.

**Option A — reuse that existing namespace** (if you have access to the same Cloudflare account): nothing to do, it's already in `wrangler.toml`.

**Option B — create a new namespace** (fresh account or environment):

```bash
wrangler kv namespace create OAUTH_KV
```

Copy the `id` it prints and update `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "OAUTH_KV"
id = "<your-new-id>"
```

## Deploy

```bash
npm run deploy
# or: npx wrangler deploy
```

Wrangler builds and deploys the Worker. On success it prints the URL:

```
https://siteimprove-mcp.<your-subdomain>.workers.dev
```

## Local development

```bash
npm run dev
# or: npx wrangler dev
```

Runs the Worker locally on `http://localhost:8787`. The OAuth flow works locally too — Wrangler spins up a local KV store.

## Type-check without deploying

```bash
npx tsc --noEmit
```

## Connect to Claude.ai

You'll need a Siteimprove account and API key (find it under **Profile → API Access** in the Siteimprove UI).

1. Open **Claude.ai → Settings → Integrations** (or the MCP server panel in your client)
2. Add a remote MCP server with URL:
   ```
   https://siteimprove-mcp.ricflams.workers.dev/mcp
   ```
   (or your own deployment URL if self-hosting)
3. Claude will redirect you through an OAuth flow — enter your Siteimprove email and API key when prompted
4. After authorising, Claude has access to all ~530 Siteimprove tools

## Notes

- The OAuth session (access token) is stored in the KV namespace. Revoking access means deleting the KV entry or rotating your Siteimprove API key.
- The Siteimprove OpenAPI spec is fetched once per warm Worker instance and cached in memory. A cold start fetches it fresh.
- Tool names are truncated to 47 characters (Claude.ai appends a 17-char suffix to a 64-char total limit). Names that exceed 47 chars use a djb2 hash suffix — see `src/toToolName.ts`.
- To adapt this for a different OpenAPI-backed API, only `src/index.ts` needs to change (spec URL, skipPath filter, toolName function, validateCredentials, loginPage HTML).
