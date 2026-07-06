import { createOpenApiMcpWorker } from "./framework.js";
import { toToolName } from "./toToolName.js";

const esc = (s: string) => (s ?? "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");

export default createOpenApiMcpWorker({
  specUrl: "https://api.siteimprove.com/v2/documentation/openapi_spec",

  skipPath: (p) => p.includes("/accessibility") || (p.includes("/seo/") && !p.includes("/seov2/")),

  toolName: toToolName,

  validateCredentials: (email, apiKey) =>
    fetch("https://api.siteimprove.com/v2/", { headers: { Authorization: "Basic " + btoa(`${email}:${apiKey}`) } })
      .then(r => r.status !== 401 && r.status !== 403).catch(() => false),

  loginPage: (params, status = 200) => {
    const q = new URLSearchParams(params).toString();
    return new Response(`<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Connect Siteimprove</title>
<style>body{font-family:system-ui,sans-serif;max-width:400px;margin:80px auto;padding:0 1rem}input,button{display:block;width:100%;margin-top:.5rem;padding:.5rem;font-size:1rem}button{background:#005fcc;color:#fff;border:none;cursor:pointer}.err{color:#c00}</style></head>
<body><h1>Connect Siteimprove</h1>
<p>Create your API key under <strong>Profile → API Access</strong> in Siteimprove.</p>
${params["error"] ? `<p class="err">${esc(params["error"])}</p>` : ""}
<form method="POST" action="/authorize?${q}">
  <label>Email<input type="email" name="email" required autocomplete="email" autofocus></label>
  <label>API key<input type="password" name="api_key" required></label>
  <button>Connect</button>
</form></body></html>`, { status, headers: { "Content-Type": "text/html;charset=UTF-8" } });
  },
});
