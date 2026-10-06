# adv Project Guide

## Scope and privacy

- This is the standalone public repository for synthesized Cardputer knowledge.
- `sources/` is local-only and must never be tracked, staged, committed, or published.
- `kb/` contains synthesized, provenance-linked Markdown suitable for public release.
- Check source licenses and remove secrets, personal data, private network details, and unlicensed excerpts before publishing.
- Do not store device credentials, raw logs, or unredacted operational captures here.

## Knowledge workflow

- Preserve source identity and citations when synthesizing claims into `kb/`.
- Keep original source material only in ignored `sources/`; do not copy whole books or repositories into `kb/`.
- Validate structural changes with `kb-bootstrap validate --dir kb --project-root .` when the tool is available.
- QMD is optional local search; `.qmd/` state is ignored.

## Git safety

- This directory is an independent Git repository nested within the `servers_team` workspace.
- Run Git commands from this directory and stage exact allowlisted paths; never use broad parent-repository staging.
- Confirm `git status --ignored` and that no `sources/` path is tracked before each commit or push.
