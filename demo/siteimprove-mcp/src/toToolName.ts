const ABBREVS: [string, string][] = [
  ["quality_assurance", "qa"],
  ["organisations", "orgs"],
  ["organisation", "org"],
  ["history", "hist"],
  ["duplicate", "dup"],
  ["documents", "docs"],
  ["attribute", "attr"],
  ["referring", "ref"],
  ["traffic_sources", "traffic"],
  ["readability_tests", "readability"],
  ["social_media", "social"],
  ["search_engines", "search_eng"],
  ["operating_systems", "os"],
  ["event_tracking", "events"],
  ["user_feedback", "feedback"],
  ["flesch_kincaid", "flesch_k"],
];

function djb2(s: string): string {
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = (((h << 5) + h) ^ s.charCodeAt(i)) >>> 0;
  return h.toString(36).padStart(6, "0").slice(-6);
}

export function toToolName(method: string, path: string): string {
  const trailingParam = /\/\{[^}]+\}$/.test(path);
  const p = path.replace(/\{[^}]+\}/g, "_");
  const prefix = method === "get" ? "" : method + "_";
  let full = (prefix + p).toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/_+/g, "_").replace(/^_+|_+$/g, "");
  for (const [from, to] of ABBREVS) full = full.split(from).join(to);
  full = full.replace(/_+/g, "_").replace(/^_+|_+$/g, "");
  if (trailingParam) full += "_";

  const pathPart = method !== "get" ? full.slice(method.length + 1) : full;
  let result: string;
  if (pathPart.startsWith("sites_") && pathPart.length > 6) {
    const stripped = pathPart.slice(6);
    result = method !== "get" ? `${method}_${stripped}` : stripped;
  } else if (pathPart === "sites" || pathPart === "sites_") {
    result = full;
  } else if (method === "get") {
    result = `_${pathPart}`;
  } else {
    result = full;
  }

  result = result.replace("integrations_", "").replace(/_traffic_/g, "_").replace(/__+/g, "_");
  const d1 = result.indexOf("domains");
  if (d1 !== -1) {
    const d2 = result.indexOf("domains", d1 + 7);
    if (d2 !== -1) result = result.slice(0, d2).replace(/_+$/, "") + result.slice(d2 + 7);
    result = result.replace(/__+/g, "_");
  }

  return result.length <= 47 ? result : result.slice(0, 40) + "_" + djb2(result);
}
