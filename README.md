# agenticweb-data

**Canonical Open Dataset, JSON Schemas, Bi-Temporal Change Log & Executable Probe Rules for [`agenticweb.wiki`](https://agenticweb.wiki)**

[![Live Site](https://img.shields.io/badge/Live_Registry-agenticweb.wiki-4E85BF)](https://agenticweb.wiki)
[![Live MCP Endpoint](https://img.shields.io/badge/MCP_Endpoint-agenticweb.wiki%2Fmcp-2ea44f)](https://agenticweb.wiki/mcp)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](LICENSE)

Maintained by [**Belgravia Labs LLC**](https://belgravialabs.com) (`info@belgravialabs.com`), `agenticweb-data` is the verified, schema-enforced ground-truth repository powering [**agenticweb.wiki**](https://agenticweb.wiki) (`INSTANCE 01` on the **Belgravia Pointer & Ontology Engine**).

Every merged commit on `main` is validated in CI against strict JSON Schemas and automatically ingested by our synchronization engine to rebuild the public registry, 52 head-to-head protocol comparisons, and the 10-tool Model Context Protocol (MCP) server at `https://agenticweb.wiki/mcp`.

---

## What Lives in This Repository

| File / Directory | Description | Schema |
| :--- | :--- | :--- |
| **`protocols.json`** | Canonical records for **103+ agentic-web standards, specifications, IETF drafts, and conventions** across 9 functional layers (`discover`, `identify`, `permit`, `read`, `act`, `coordinate`, `pay`, `present`, `account`). Every claim carries primary-source `evidence[]` pointers and verification confidence (`VERIFIED`, `REPORTED`, `THIN`). | `schema/protocols.schema.json` |
| **`probes.json`** | Executable HTTP probe rules (`GET` paths, headers, JSONPath/regex matchers, and SSRF-safe origin validation rules) used by the live `/check/<domain>/` scanner and `probe` MCP tool. | `schema/probes.schema.json` |
| **`changes.json`** | Bi-temporal change ledger recording specification version bumps, IETF draft expirations/renewals, working-group adoptions, and status transitions with `observed_at` and source evidence pointers. | `schema/changes.schema.json` |
| **`instances.json`** | Verified live production deployments (`VERIFIED` via active HTTP probe or primary-source link check) implementing agentic-web protocols in the wild. | `schema/instances.schema.json` |
| **`resources.json`** & **`useful-resources.json`** | Conformance validators, SDKs, registries, and reference implementations mapped by protocol ID. | `schema/resources.schema.json` |
| **`terms.json`** & **`vocab.json`** | Controlled ontology vocabulary, functional taxonomy, and canonical glossary definitions. | `schema/terms.schema.json`, `schema/vocab.schema.json` |
| **`census.json`** | Empirical origin-probe adoption census snapshots across top web domains (`/.well-known/ard.json`, `/.well-known/ai-catalog.json`, `/.well-known/mcp.json`, `/llms.txt`, etc.). | — |
| **`scripts/validate.py`** | Deterministic schema, cross-reference, vocabulary, and URL validator executed on every pull request and automated watcher commit. | — |

---

## Querying This Data via Live MCP (`https://agenticweb.wiki/mcp`)

You can query this dataset—and run live origin probes against any domain—directly from your AI agent via the stateless streamable HTTP MCP endpoint at **`https://agenticweb.wiki/mcp`**.

### Available MCP Tools (10)
- `define` — Retrieve the canonical definition and cross-references for an agentic-web term or protocol.
- `get` — Fetch the full structured record, status model, evidence pointers, and probe rule for a standard.
- `search` — Full-text and facet search across standards, glossary terms, and verified instances.
- `ask` — Deterministic protocol recommendation and architectural ranking for a given agent use case and audience.
- `has` — Check which domains or instances implement a specific standard.
- `probe` — Execute live SSRF-guarded HTTP probes against a target domain and return its agent-readiness scorecard.
- `validate_manifest` — Validate an `ard.json`, `mcp.json`, or `agent.json` manifest against normative JSON Schemas.
- `template` — Generate ready-to-deploy manifest templates (`ard.json`, `llms.txt`, `AGENTS.md`, SEP-2127 MCP server card).
- `changes` — Query recent specification version diffs and status changes from the bi-temporal ledger.
- `stale` — Audit records approaching verification expiry or IETF Internet-Draft expiration.

---

## Local Validation & Contributing

See [**CONTRIBUTING.md**](CONTRIBUTING.md) for evidence grading rules (`VERIFIED` vs. `REPORTED` vs. `THIN`) and how our automated freshness watchers (`agenticweb-bot`) interact with human pull requests.

To run the deterministic validator locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install jsonschema
python3 scripts/validate.py
```

---

## License

All data in this repository is licensed under [**Creative Commons Attribution 4.0 International (CC BY 4.0)**](LICENSE).
Maintained by [**Belgravia Labs LLC**](https://belgravialabs.com) · [info@belgravialabs.com](mailto:info@belgravialabs.com).
