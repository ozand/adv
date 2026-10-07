# adv Project Guide

## Required reading

Before starting work, read:
- [GOALS.md](GOALS.md) for strategic vision, goals, desired outcomes, and boundaries.
- [README.md](README.md) for a concise repository overview.
- [docs/adr/INDEX.md](docs/adr/INDEX.md) and any relevant accepted ADR before changing architecture, publication boundaries, source handling, or canonical data contracts.
- The governing open GitHub Issue and its linked PRD/design/ADR records before implementation.

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

## Issue, PRD, ADR, and PR workflow

- Every new task or independently testable follow-up must have a matching open GitHub Issue before implementation. Work only within that Issue's scope and acceptance criteria; create/update a separate Issue before expanding scope.
- Use the Issue as the execution record: problem, context/provenance, scope, exclusions, acceptance criteria, verification, dependencies, and safety constraints. Link the Issue from any planning/design artifacts and from the pull request.
- Create a PRD or focused requirements/design note when an Issue has unresolved user needs, workflows, measurable outcomes, or substantial feature behavior that needs agreement before implementation. Keep it proportional; do not create a PRD for a straightforward documentation fix.
- Create an ADR before changing architecture, public contracts, data formats, dependencies, trust/publication boundaries, or another decision whose rationale should persist. Use the existing append-only ADR series under `docs/adr/` and update its index.
- Implement on a task branch/worktree as project governance permits. Open a reviewed PR referencing the Issue; include acceptance evidence, focused tests/validation, and any residual risks. Do not self-merge unless explicitly authorized.
- Keep Issue status truthful. Use the repository's `in progress` label only after work actually starts; remove it when work is paused/completed according to repository policy.
- Do not commit or push unless explicitly authorized by the owner or governing project workflow.

## Git safety

- This directory is an independent Git repository nested within the `servers_team` workspace.
- Run Git commands from this directory and stage exact allowlisted paths; never use broad parent-repository staging.
- Confirm `git status --ignored` and that no `sources/` path is tracked before each commit or push.
