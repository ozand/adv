# ADR-001: Publish synthesized knowledge in a separate public repository

**Status**: Accepted
**Date**: 2026-10-06
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: Issue #227

## Context

The Cardputer project lives under `Project/servers/adv/` in the `servers_team` workspace, whose worktree contains unrelated local changes. The owner wants a public repository for synthesized knowledge about multiple Cardputer projects, while source repositories, web captures, and books remain local-only. A separate Git root prevents parent repository changes from being included and provides an explicit publication boundary.

The public/private choice and source exclusion were confirmed by the owner in this session. Private local network details are intentionally excluded from this public ADR.

## Decision

Use `ozand/adv` as a standalone public Git repository rooted at this directory. Keep cloned repositories, books, and other source material under an entirely ignored local-only `sources/` directory. Track only reviewed, synthesized and cited knowledge in `kb/` and project governance/documentation files.

### What this IS

A public knowledge repository with local private research inputs and published synthesized outputs.

### What this IS NOT

A mirror/archive of source repositories, books, web pages, device credentials, or raw operational logs. It does not assert that the Cardputer address is reachable.

## Consequences

### What gets easier

- Knowledge can be shared independently from the parent workspace.
- Private source inputs stay outside the public Git history.

### What gets harder

- Every synthesized note needs provenance and license review.
- Contributors must verify ignore and staging boundaries before publication.
- Local source materials require separate backup and cannot be recovered from GitHub.

### What does not change

The existing `servers_team` worktree and its unrelated changes remain untouched. No source material is authorized for publication.

## Alternatives Considered

### Keep `adv` inside `servers_team`

This couples the knowledge lifecycle to the parent workspace and its unrelated changes, contrary to the requested standalone public project.

### Publish source material alongside the KB

Rejected because source clones/books are explicitly local-only and may carry licensing or privacy constraints.

## Test Contract

| Claim in Decision | Test | Currently |
|---|---|---|
| Sources are ignored and not tracked | `git check-ignore -v sources/README.md`; inspect `git ls-files sources` | Passing: ignored; no source files tracked |
| KB structure conforms to bootstrap contract | `kb-bootstrap validate --dir kb --project-root .` | Blocked: installed CLI fails to import `kb_bootstrap.cli` |
| Public remote points to intended repository | `gh repo view ozand/adv`; `git remote -v` | Passing: public repo verified; `origin` points to it |

## Rollback

The local repository can be detached from its remote, but public content may have been cloned or cached. Removing files or deleting a GitHub repository cannot guarantee erasure of previously published content.

## References

- User request and confirmations in this session
- [Issue #227](https://github.com/ozand/servers_team/issues/227)
- [kb-bootstrap](https://github.com/ozand/kb-bootstrap)
