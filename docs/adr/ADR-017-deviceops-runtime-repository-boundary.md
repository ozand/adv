# ADR-017: Keep DeviceOps runtime artifacts outside the `adv` knowledge repository

**Status:** Accepted — owner approved `ozand/deviceops` and local path on 2026-10-12. Publication and hardware use remain separately gated.
**Date:** 2026-10-12.
**Issue:** [#68](https://github.com/ozand/adv/issues/68).
**Supersedes:** None.
**Related:** ADR-007, ADR-014, ADR-015, ADR-016.

## Context

The `adv` project is a public Cardputer knowledge repository. ADR-007 distinguishes reviewed knowledge from local source originals. A persistent DeviceOps service would add executable source, dependency locks, releases and operational state, with a different release and trust lifecycle. Issue #68 asks whether implementation belongs in `adv` and requires a concrete path boundary. The owner named the destination and recorded authorization before its creation.

## Decision

### What this IS

Keep `adv` for architecture/decision documents and coordination. Use the private repository `ozand/deviceops` for runtime source, tests, manifests and lockfiles; binary releases should use reviewed GitHub Releases artifacts rather than commit binaries into either source repository. The owner approved the identity, local clone path `T:/Code/esp32/deviceops`, and path allowlist: `/deviceops/` for service source, `/tests/`, `/docs/`, and root manifests/locks. The repository was created private and bootstrapped; this ADR authorizes no unrelated code transfer. Device bindings, databases, ports, logs, credentials and operational captures stay local/private, never in either public repository.

### What this IS NOT

Does not authorize public release, code transfer from `adv`, packages, binaries, hardware or network activity; ADR-007 evidence/publication rules remain in force.

### Success criteria

Owner approval is recorded in Issue #68. Bootstrap commit `e56fd6a628a6bd7137b4adb48b8c646f7674263d` contains only README, contributor governance and a minimal Python project manifest. Subsequent PRs must verify exact path scope and contain no private operational data.

## Consequences

### What gets easier

Knowledge publication and runtime releases can be reviewed, versioned and secured independently.

### What gets harder

Cross-repository references, issue coordination, version compatibility and release provenance need explicit maintenance.

### What does not change

Existing firmware contracts, hardware authorization and evidence requirements remain unchanged.

## Alternatives Considered

- **Keep runtime source in `adv`:** rejected because runtime lifecycle and executable artifacts conflict with the knowledge-only project boundary.
- **Publish runtime source immediately:** rejected because the approved bootstrap is private and publication requires separate approval.

## Test Contract

| Claim | Test | Currently |
|---|---|---|
| `adv` changes contain no runtime artifacts | exact changed-path allowlist review | required for each PR; not automated |
| Runtime destination is owner-approved | owner receipt plus verified repository/path | satisfied for private bootstrap; implementation scope remains issue-gated |
| Private runtime state is excluded from publication | staged-path and secret/privacy review | required for future runtime PRs |

## Rollback

Acceptance recorded 2026-10-12. Changing this boundary requires a superseding ADR and explicit migration/release plan.

## References

Issue #68, ADR-007, ADR-014, DeviceOps architecture and project AGENTS.md.
