# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in **agenticweb.wiki**, its Model Context Protocol (MCP) server (`https://agenticweb.wiki/mcp`), its origin probe (`agenticweb-probe/1.0`), or the `agenticweb-data` dataset and schemas:

- **Email:** [info@belgravialabs.com](mailto:info@belgravialabs.com)
- **RFC 9116 `security.txt`:** [`https://agenticweb.wiki/.well-known/security.txt`](https://agenticweb.wiki/.well-known/security.txt)

Please include the affected endpoint or file path, reproduction steps, and impact assessment. We acknowledge vulnerability reports within **48 hours** and aim to ship verified remediations within **7 days**.

## Scope & Safety Architecture

1. **Read-Only & Stateless MCP Server (`https://agenticweb.wiki/mcp`):**
   - All 11 MCP tools are strictly read-only (`readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`).
2. **SSRF & Origin Protection on Live Probes (`has`, `probe`, `validate_manifest`, `/check/`):**
   - All user-supplied origins are resolved via DNS-over-HTTPS (DoH) prior to socket connection; RFC 1918 private ranges, loopback (`127.0.0.0/8`, `::1`), link-local (`169.254.0.0/16`), CGNAT, and metadata IPs are hard-blocked (`invalid-origin`).
   - Per-client (`PROBE_LIMIT`, `HAS_LIMIT`) and per-target-IP (`TARGET_LIMIT`) rate limiters fail closed to prevent amplification.
   - Site operators may opt out of probing at any time by disallowing `User-agent: agenticweb-probe` in `/robots.txt`.
