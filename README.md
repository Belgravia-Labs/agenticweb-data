# agenticweb-data (`wiki.agenticweb/probe`)

**Canonical Open Dataset, JSON Schemas, Bi-Temporal Change Log, Executable Probe Rules & Stateless MCP Server (`https://agenticweb.wiki/mcp`) for [`agenticweb.wiki`](https://agenticweb.wiki)**

[![Live Site](https://img.shields.io/badge/Live_Registry-agenticweb.wiki-4E85BF)](https://agenticweb.wiki)
[![Live MCP Endpoint](https://img.shields.io/badge/MCP_Endpoint-agenticweb.wiki%2Fmcp-2ea44f)](https://agenticweb.wiki/mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data-CC_BY_4.0-lightgrey.svg)](LICENSE)

Maintained by [**Belgravia Labs LLC**](https://belgravialabs.com) (`info@belgravialabs.com`), `agenticweb-data` is the verified, schema-enforced ground-truth repository powering [**agenticweb.wiki**](https://agenticweb.wiki) and its public Model Context Protocol (MCP) server **`wiki.agenticweb/probe`** at **`https://agenticweb.wiki/mcp`**.

Every merged commit on `main` is validated in CI against strict JSON Schemas and automatically ingested to rebuild the public registry (**133 standards**, **49 glossary terms**, **52 head-to-head comparisons**, **236+ probed origins**) and the **11-tool stateless Streamable HTTP MCP server**.

---

## Connect to the MCP Server (`https://agenticweb.wiki/mcp`)

- **Transport:** Stateless Streamable HTTP (`POST https://agenticweb.wiki/mcp`, MCP `2026-07-28` specification; also backward-compatible with `2025-11-25`, `2025-06-18`, and `2025-03-26`).
- **Authentication:** None required (public read-only endpoint).
- **SEP-2127 Server Card:** [`https://agenticweb.wiki/mcp/server-card`](https://agenticweb.wiki/mcp/server-card) (`application/mcp-server-card+json`)
- **ARD 1.0 Manifest:** [`https://agenticweb.wiki/.well-known/ard.json`](https://agenticweb.wiki/.well-known/ard.json)

### Quick Configuration (`claude_desktop_config.json` / `.mcp.json` / Cursor)

```json
{
  "mcpServers": {
    "agenticweb": {
      "type": "http",
      "url": "https://agenticweb.wiki/mcp"
    }
  }
}
```

```bash
claude mcp add --transport http agenticweb https://agenticweb.wiki/mcp
```

---

## Tools (`tools/list` & `tools/call` — 11 Tools)

All 11 tools are deterministic, read-only (`readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`), and execute at the Cloudflare edge in `<15 ms`.

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| **`define`** | `term: string` | Define an agentic-web glossary term (49 terms) or standard (133 protocols) by id, name, or alias. Returns `definition_md`, `related_protocols`, and `standard_summary_md`. |
| **`get`** | `id: string` | Fetch one standard's complete record by id (`"mcp"`), acronym (`"A2A"`), RFC (`"RFC 9421"`), or well-known path (`"llms.txt"`, `"/.well-known/ard.json"`): status, governance, version, spec URL, probe rule, evidence, disputes, and freshness. |
| **`search`** | `q?: string`, `query?: string` | Search all 133 standards and 49 glossary terms by name, acronym, alias, question, or use case (`"A2A vs MCP"`, `"mcp.auth"`). Returns top 10 matches plus `nearest_ids` and `nearest_terms` on misses. |
| **`ask`** | `question?: string`, `q?: string`, `use_case?: string`, `audience?: string` | Recommend and rank standards to implement for an engineering goal (`"let agents pay per request"`), or compare named protocols head-to-head with `/compare/<slug>/` links. |
| **`has`** | `origin: string`, `id: string` | Live-check a public origin for one standard (`"llms-txt"`, `"ard"`, `"mcp-server-cards"`). Returns `found`, `url`, `status`, `reason`, and `article`. |
| **`probe`** | `origin: string`, `compact?: boolean` | Live-scan a public origin across ~30 agent-facing standards in parallel (24h KV cached). Pass `compact: true` to return `absent_ids[]` instead of full absent/skipped maps (~85% smaller). |
| **`validate_manifest`** | `origin: string`, `id?: string`, `compact?: boolean` | Validate an origin's 12 agent manifests (`ard`, `ai-catalog-well-known-file`, `mcp-server-cards`, `a2a`, `llms-txt`, `agents-md`, `anthropic-agent-skills-format`, `api-catalog-rfc9727`, `ai-crawler-tokens-robots`, `security-txt`, `auth-md`, `okf`) against specs, grade readiness (`A+` to `F`), and return `agent_routing`. Pass `compact: true` to omit nested probe and absent manifests. |
| **`template`** | `id: string`, `domain?: string`, `name?: string`, `description?: string`, `mcp_url?: string`, `api_url?: string`, `agent_url?: string`, `contact?: string` | Generate spec-compliant starter boilerplate (`contents`, `target_path`, `content_type`, `recommended_headers`) for any of the 10 publishable agent manifests. |
| **`changes`** | `since: string`, `step?: string`, `record_id?: string`, `limit?: number` | Query machine-verified changelog diffs (`old` -> `new`, summary, evidence URL, date) since `YYYY-MM-DD`. |
| **`stale`** | `days?: number`, `step?: string` | List standards whose `last_verified` date is older than `days` (default `30`), optionally filtered by lifecycle step. |
| **`digest`** | `date?: string`, `list?: boolean`, `compact?: boolean`, `include_stats?: boolean` | Fetch the daily Agentic Web Digest (`date: "latest"` or `"YYYY-MM-DD"`), list all published dates (`list: true`), or pass `compact: true` / `include_stats: false` to omit the stats block. |

### Example JSON-RPC 2.0 Calls

```bash
# 1. Define a term or protocol
curl -sS -X POST https://agenticweb.wiki/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"define","arguments":{"term":"MCP"}}}'

# 2. Validate a domain in compact mode
curl -sS -X POST https://agenticweb.wiki/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"validate_manifest","arguments":{"origin":"cloudflare.com","compact":true}}}'
```

---

## MCP Resources (`resources/list` & `resources/read` — 4 Resources)

- `agenticweb://standards/all` — All 133 protocol records + the 9-step facet vocabulary (`https://agenticweb.wiki/data/standards.json`).
- `agenticweb://glossary/all` — All 49 glossary terms with definitions, aliases, and sources (`https://agenticweb.wiki/data/terms.json`).
- `agenticweb://use-cases/all` — All 15 engineering use cases mapped to the standards that serve them.
- `agenticweb://probes/all` — All 133 probe rules and skip reasons (`https://agenticweb.wiki/data/probes.json`).

## MCP Prompts (`prompts/list` & `prompts/get` — 3 Workflows)

- `audit-domain` (`{ domain }`) — Audit a domain's manifests, explain spec violations, and recommend the 3 highest-impact missing files.
- `make-repo-agent-ready` (`{ domain, project_type? }`) — Generate all agent-facing files for a repository using `template()`.
- `compare-protocols` (`{ first, second }`) — Compare two standards side-by-side across all 12 schema dimensions.

---

## Repository Contents

| File / Directory | Description | Schema |
| :--- | :--- | :--- |
| **`protocols.json`** | Canonical records for **133 agentic-web standards, specifications, IETF drafts, and conventions** across 9 lifecycle steps (`discover`, `identify`, `permit`, `read`, `act`, `coordinate`, `pay`, `present`, `account`). | `schema/protocols.schema.json` |
| **`terms.json`** | **49 technical glossary terms** with multi-paragraph definitions, aliases, related protocol IDs, and verified sources. | `schema/terms.schema.json` |
| **`probes.json`** | Executable HTTP probe rules used by `/check/<domain>/`, `probe`, `has`, and `validate_manifest`. | `schema/probes.schema.json` |
| **`changes.json`** | Bi-temporal change ledger recording specification version bumps, draft renewals, and status transitions. | `schema/changes.schema.json` |
| **`instances.json`** | Verified live production deployments implementing agentic-web protocols in the wild. | `schema/instances.schema.json` |
| **`census.json`** | Empirical origin-probe adoption census across **236+ probed domains**. | — |
| **`digests/` & `stats/`** | Daily cited Agentic Web Digest issues and panel adoption telemetry snapshots. | `schema/digest.schema.json` |
| **`server.json`** | Official MCP Registry descriptor (`wiki.agenticweb/probe`, v1.2.0). | — |

---

## Security & License

- **Security Policy:** See [**SECURITY.md**](SECURITY.md) or [`https://agenticweb.wiki/.well-known/security.txt`](https://agenticweb.wiki/.well-known/security.txt).
- **License:** Code, JSON Schemas, probe rules, and MCP definitions are licensed under the [**MIT License**](LICENSE). Editorial prose summaries are dual-licensed under **MIT** and **CC BY 4.0**.
