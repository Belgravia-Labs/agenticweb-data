#!/usr/bin/env python3
"""Validate every data file against its schema and the vocab. Exit 1 on the first error.
Run: python3 scripts/validate.py [--urls]  (--urls also HEAD-checks evidence URLs added since origin/main)"""
from __future__ import annotations
import json, sys, subprocess, urllib.request
from pathlib import Path
import jsonschema

FILES = {"vocab.json": "vocab", "protocols.json": "protocols", "terms.json": "terms", "resources.json": "resources",
         "useful-resources.json": "useful-resources", "instances.json": "instances", "news.json": "news",
         "probes.json": "probes", "changes.json": "changes"}
VOCAB_FIELDS = {"step": "steps", "form": "form", "track": "track", "scope": "scope", "phase": "phase",
                "implementation": "implementation"}
LIST_FIELDS = {"parties": "parties", "use_cases": "use_cases", "audience": "audience"}

def load(root: Path, name: str):
    return json.loads((root / name).read_text())

def check(root: Path) -> list[str]:
    errors: list[str] = []
    data = {}
    for fname, sname in FILES.items():
        schema_path = root / "schema" / f"{sname}.schema.json"
        if not (root / fname).exists():
            errors.append(f"missing {fname}"); continue
        try:
            data[fname] = load(root, fname)
            jsonschema.validate(data[fname], load(root, f"schema/{sname}.schema.json") if schema_path.exists() else {})
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            errors.append(f"{fname}: {getattr(e, 'message', e)}")
    if errors: return errors
    vocab = data["vocab.json"]
    ids = {k: {i["id"] for i in v} for k, v in vocab.items()}
    recs = data["protocols.json"]
    rec_ids = [r["id"] for r in recs]
    if len(rec_ids) != len(set(rec_ids)): errors.append("protocols.json: duplicate ids")
    known = set(rec_ids)
    for r in recs:
        for f, vk in VOCAB_FIELDS.items():
            if r.get(f) is not None and r[f] not in ids[vk]: errors.append(f"{r['id']}: {f}={r[f]!r} not in vocab.{vk}")
        for f, vk in LIST_FIELDS.items():
            for v in r.get(f) or []:
                if v not in ids.get(vk, set()): errors.append(f"{r['id']}: {f} value {v!r} not in vocab.{vk}")
        if r["adoption"]["level"] not in ids["adoption"]: errors.append(f"{r['id']}: adoption.level not in vocab")
        for ev in r["evidence"]:
            if ev["label"] not in ids["evidence"]: errors.append(f"{r['id']}: evidence label {ev['label']!r}")
        for f in ("pairs_with", "prerequisites"):
            for pid in r.get(f) or []:
                if pid not in known: errors.append(f"{r['id']}: {f} unknown id {pid}")
        if r.get("freshness") is not None and r["freshness"] not in ids["freshness"]: errors.append(f"{r['id']}: freshness not in vocab")
    for pid in data["resources.json"]:
        if pid not in known: errors.append(f"resources.json: unknown id {pid}")
    for t in data["terms.json"]:
        if t["id"] in known: errors.append(f"terms.json {t['id']}: id collides with a protocol id (terms and protocols share one search index)")
    for t in data["terms.json"]:
        for pid in t.get("related_protocols", []):
            if pid not in known: errors.append(f"terms.json {t['id']}: unknown id {pid}")
    for fname, field in (("useful-resources.json", "covers"), ("instances.json", "implements"), ("news.json", "related")):
        for rec in data[fname]:
            for pid in rec.get(field, []):
                if pid not in known: errors.append(f"{fname}: unknown id {pid}")
    for row in data["changes.json"]:
        if row["record_id"] not in known: errors.append(f"changes.json {row['id']}: unknown id {row['record_id']}")
    probes = data["probes.json"]
    if set(probes) != known: errors.append(f"probes.json: ids differ from protocols.json: {sorted(set(probes) ^ known)[:5]}")
    return errors

def new_evidence_urls(root: Path) -> list[str]:
    """Evidence URLs present in the working tree but not in origin/main's protocols.json."""
    try:
        old = json.loads(subprocess.run(["git", "show", "origin/main:protocols.json"], cwd=root, capture_output=True, text=True, check=True).stdout)
    except subprocess.CalledProcessError:
        return []
    seen = {ev["url"] for r in old for ev in r["evidence"]}
    return sorted({ev["url"] for r in load(root, "protocols.json") for ev in r["evidence"] if ev["url"] not in seen})

def url_ok(url: str) -> bool:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 agenticweb-data-ci"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r: return 200 <= r.status < 400
    except Exception:
        return False

def main(root: Path, check_urls: bool = False) -> int:
    errors = check(root)
    if check_urls and not errors:
        for u in new_evidence_urls(root):
            if not url_ok(u): errors.append(f"new evidence URL not reachable: {u}")
    for e in errors: print("ERROR:", e)
    print("ok" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main(Path(__file__).resolve().parents[1], "--urls" in sys.argv))
