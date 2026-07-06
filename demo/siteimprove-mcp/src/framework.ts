import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { WorkerEntrypoint } from "cloudflare:workers";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPTransport } from "@hono/mcp";
import { Hono } from "hono";
import { z } from "zod";

// ── Types ─────────────────────────────────────────────────────────────────────

export interface Param {
  name: string; in: string; required?: boolean;
  type?: string; description?: string;
  schema?: { properties?: Record<string, unknown>; required?: string[] };
}
export interface Op { summary?: string; description?: string; parameters?: Param[] }
export interface Tool { name: string; desc: string; method: string; path: string; params: Param[] }

export interface OpenApiMcpConfig {
  specUrl: string;
  skipPath?: (path: string) => boolean;
  toolName?: (method: string, path: string) => string;
  validateCredentials: (email: string, apiKey: string) => Promise<boolean>;
  loginPage: (params: Record<string, string>, status?: number) => Response;
}

// ── Generic helpers ────────────────────────────────────────────────────────────

export function zodSchema(params: Param[]) {
  const shape: Record<string, z.ZodType> = {};
  for (const p of params) {
    if (p.in === "header") continue;
    if (p.in === "body") { for (const k of Object.keys(p.schema?.properties ?? {})) shape[k] = z.unknown(); continue; }
    const base = p.type === "integer" || p.type === "number" ? z.number() : p.type === "boolean" ? z.boolean() : z.string();
    shape[p.name] = (p.required ? base : base.optional()).describe(p.description ?? "");
  }
  return shape;
}

export async function callTool(tool: Tool, args: Record<string, unknown>, baseUrl: string, auth: string) {
  let url = baseUrl + tool.path;
  const query: Record<string, string> = {};
  const body: Record<string, unknown> = {};
  const bodyKeys = new Set(tool.params.filter(p => p.in === "body").flatMap(p => Object.keys(p.schema?.properties ?? {})));
  for (const p of tool.params) {
    const v = args[p.name];
    if (p.in === "path")       url = url.replace(`{${p.name}}`, v != null ? encodeURIComponent(String(v)) : `{${p.name}}`);
    else if (p.in === "query" && v != null) query[p.name] = String(v);
  }
  for (const k of bodyKeys) if (args[k] !== undefined) body[k] = args[k];
  const qs = new URLSearchParams(query).toString();
  if (qs) url += "?" + qs;
  const hasBody = Object.keys(body).length > 0;
  const res = await fetch(url, { method: tool.method.toUpperCase(), headers: { Authorization: auth, Accept: "application/json", ...(hasBody ? { "Content-Type": "application/json" } : {}) }, ...(hasBody ? { body: JSON.stringify(body) } : {}) });
  const text = await res.text();
  return res.ok ? text : `HTTP ${res.status}: ${text}`;
}

// ── Factory ────────────────────────────────────────────────────────────────────

function defaultToolName(method: string, path: string): string {
  const prefix = method === "get" ? "" : method + "_";
  return (prefix + path).toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/_+/g, "_").replace(/^_+|_+$/g, "").slice(0, 64);
}

export function createOpenApiMcpWorker(config: OpenApiMcpConfig) {
  const nameFn = config.toolName ?? defaultToolName;
  let cache: { tools: Tool[]; baseUrl: string } | null = null;

  async function getSpec() {
    if (cache) return cache;
    const spec = await fetch(config.specUrl).then(r => r.json()) as Record<string, unknown>;
    const tools: Tool[] = [];
    for (const [path, methods] of Object.entries(spec["paths"] as Record<string, Record<string, Op>>)) {
      if (config.skipPath?.(path)) continue;
      for (const [method, op] of Object.entries(methods)) {
        if (!["get", "post", "put", "patch", "delete"].includes(method)) continue;
        tools.push({ name: nameFn(method, path), desc: ([op.summary, op.description].filter(Boolean).join("\n") || path).slice(0, 1024), method, path, params: op.parameters ?? [] });
      }
    }
    // Swagger 2.0 uses host+basePath; OpenAPI 3.0 uses servers[0].url
    const baseUrl = spec["servers"]
      ? (spec["servers"] as { url: string }[])[0]?.url ?? ""
      : `https://${spec["host"]}${spec["basePath"] ?? ""}`;
    return (cache = { tools, baseUrl });
  }

  class McpHandler extends WorkerEntrypoint {
    async fetch(request: Request) {
      const { email, apiKey } = this.ctx.props as { email: string; apiKey: string };
      const auth = "Basic " + btoa(`${email}:${apiKey}`);
      const { tools, baseUrl } = await getSpec();
      const server = new McpServer({ name: "openapi-mcp", version: "0.1.0" });
      for (const tool of tools) {
        server.tool(tool.name, tool.desc, zodSchema(tool.params), async (args) => ({
          content: [{ type: "text" as const, text: await callTool(tool, args as Record<string, unknown>, baseUrl, auth) }],
        }));
      }
      const transport = new StreamableHTTPTransport();
      if (!server.isConnected()) await server.connect(transport);
      return new Hono().all("/mcp", c => transport.handleRequest(c)).fetch(request);
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const AuthHandler = {
    async fetch(request: Request, env: any) {
      const url = new URL(request.url);
      if (url.pathname !== "/authorize") return new Response("Not found", { status: 404 });
      const params = Object.fromEntries(url.searchParams);
      if (request.method === "GET") return config.loginPage(params);
      const form = await request.formData();
      const email  = (form.get("email")   as string ?? "").trim();
      const apiKey = (form.get("api_key") as string ?? "").trim();
      const ok = await config.validateCredentials(email, apiKey);
      if (!ok) return config.loginPage({ ...params, error: "Invalid email or API key — please try again." }, 401);
      const oauthReq = await env.OAUTH_PROVIDER.parseAuthRequest(request);
      const { redirectTo } = await env.OAUTH_PROVIDER.completeAuthorization({ request: oauthReq, userId: email, scope: (oauthReq as { scope: string[] }).scope, props: { email, apiKey } });
      return Response.redirect(redirectTo, 302);
    },
  };

  return new OAuthProvider({
    apiRoute: "/mcp",
    apiHandler: McpHandler,
    defaultHandler: AuthHandler,
    authorizeEndpoint: "/authorize",
    tokenEndpoint: "/token",
    clientRegistrationEndpoint: "/register",
    scopesSupported: ["mcp"],
  });
}
