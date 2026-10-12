# ADR-017: Keep DeviceOps runtime artifacts outside the `adv` knowledge repository

**Status:** Proposed — requires owner review and acceptance.
**Date:** 2026-10-12.
**Issue:** [#68](https://github.com/ozand/adv/issues/68).
**Supersedes:** None.
**Related:** ADR-007, ADR-014, ADR-015, ADR-016.

## Context

The `adv` project is a public Cardputer knowledge repository. ADR-007 distinguishes reviewed knowledge from local source originals. A persistent DeviceOps service would add executable source, dependency locks, releases and operational state, with a different release and trust lifecycle. Issue #68 explicitly asks whether implementation belongs in `adv` and requires a concrete path boundary. The exact destination repository is not yet named or authorized.

## Decision

### What this IS

Propose that `adv` contain architecture/decision documents and coordination only. Recommend the repository `ozand/deviceops` for runtime source, tests, manifests and lockfiles; binary releases should use reviewed GitHub Releases artifacts rather than commit binaries into either source repository. This is a proposed destination, not an existing repository or a repository-creation authorization. Do not create that repository or transfer code until the owner accepts this proposed identity and a separate issue approves an exact runtime path allowlist (for example, `/deviceops/` for service source, `/tests/`, `/docs/`, and root manifests/locks). Device bindings, databases, ports, logs, credentials and operational captures stay local/private, never in either public repository.

### What this IS NOT

Does not create a repository, select its name/owner/visibility, authorize code migration or publication, or change ADR-007's evidence/publication rules.

### Success criteria

Owner approves destination identity and exact path allowlist in a separately governed task; confirm whether `T:/Code/esp32/deviceops` is the intended local clone path without creating it here. PR review confirms `adv` changes are documentation-only and contain no runtime artifacts or private operational data.

## Consequences

### What gets easier

Knowledge publication and runtime releases can be reviewed, versioned and secured independently.

### What gets harder

Cross-repository references, issue coordination, version compatibility and release provenance need explicit maintenance.

### What does not change

Existing firmware contracts, hardware authorization and evidence requirements remain unchanged.

## Alternatives Considered

- **Put service and binaries in `adv`:** rejected because runtime lifecycle and executable artifacts conflict with the knowledge-only project boundary.
- **Name/create a new repository now:** deferred because the destination identity and owner approval are not established by Issue #68.
- **Do nothing:** keeps the current boundary safe but leaves no approved implementation location; acceptable until owner decides.

## Test Contract

| Claim | Test | Currently |
|---|---|---|
| `adv` changes contain no runtime artifacts | exact changed-path allowlist review | applicable to each PR; not yet automated |
| Runtime destination is owner-approved | owner receipt plus verified repository/path | not yet available |
| Private runtime state is excluded from publication | staged-path and secret/privacy review | required for future runtime PRs |

## Rollback

Before acceptance, keep current repository structure and make no runtime move. After acceptance, changing the boundary requires a superseding ADR and explicit migration/release plan.

## References

Issue #68, ADR-007, ADR-014, DeviceOps architecture and project AGENTS.md.
