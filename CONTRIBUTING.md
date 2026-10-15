# Contributing to agenticweb-data

This repo is the data behind https://agenticweb.wiki: one record per agentic-web standard, the glossary,
news, probe rules and the change log. The site rebuilds from `main` within the hour.

## What gets a record
A standard, specification, protocol or convention that software agents or agent-ready sites can implement
against a public normative text. Products, SDKs, papers and opinions are listed as instances or resources
instead. The full rule is at https://agenticweb.wiki/methodology/.

## Evidence rules
- Every claim has an `evidence[]` item: `claim`, `label`, `url`, `date` (the source's date).
- `VERIFIED` = the issuer's own text or a standards body (IETF, W3C, Linux Foundation, FIDO, EMVCo, Ecma).
  `REPORTED` = one secondary source. `THIN` = weaker than that.
- Never remove or edit an existing evidence item; append.
- Vocabulary ids live in `vocab.json`. The validator rejects anything else.

## Bots
Watchers run daily from a server we operate and commit as `agenticweb-bot`. They change version, status,
expiry and `last_verified`, append evidence, and write `changes.json` and `news.json`. A weekly digest is
reviewed by the maintainer; wrong changes are reverted with `git revert`, and the bot never reapplies a
reverted change. Candidate records drafted by a model carry `"candidate": true` and a confidence.

## How to propose a change
1. Open an issue with the template, or a pull request.
2. Run `python3 scripts/validate.py --urls` (needs `pip install jsonschema`).
3. A maintainer merges. Merged data is live within the hour.

Data is CC BY 4.0. Maintainer: Belgravia Labs, info@belgravialabs.com.
