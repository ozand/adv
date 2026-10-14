# ADR-022: Use an owner-provisioned Git executable for qualification probes

**Status**: Accepted — owner confirmed 2026-10-14; runner correction implemented and scoped-reviewed, broader qualification pending
**Date**: 2026-10-14
**Authors**: Coding assistant
**Issue**: [#81](https://github.com/ozand/adv/issues/81)
**Supersedes**: None
**Related**: ADR-015, ADR-017, ADR-018, ADR-021

## Context

Security review of `ozand/deviceops` PR #17 exact head `396703539d3c214d9b5798f87810bf53100810b0` found that the conformance runner invokes Git by bare name through inherited `PATH`. The reviewer reported reproducing a fake Git executable claiming a clean selected SHA and no untracked pytest influencers while an untracked `tests/conftest.py` existed (#4266557209). This is a review report, not independently reproduced by this ADR author. The earlier PYTHONPATH shadowing issue is separately fixed and reviewed (#4266253197).

Published ADR-015 selects Python 3.11+ and Windows 11 x64 first, but leaves exact toolchain qualification open. ADR-017 selects the private runtime repository and file allowlist; ADR-018's OS-admin residual-threat language concerns the DeviceOps runtime authorization model, not this test runner's Git selection. No accepted ADR/D01 text identifies a trusted Git executable source or declares inherited PATH trustworthy. Thus Git identity and untracked-file probes have no defined executable trust source.

### Problem statement

Before Git output can bind a qualification receipt to source and pytest inputs, the runner needs a defined, reproducible way to select the Git executable and must fail closed if that executable or repository-root identity cannot be established.

## Decision

### What this IS

The qualification operator must provision and explicitly select an absolute Git executable path from the controlled local toolchain for the run. The runner must resolve that configured path once, reject a bare command name, invoke only that executable for all Git probes with a sanitized environment that removes inherited executable/config and repository/index selector variables including `GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`, and `GIT_INDEX_FILE`, disable the tested repository-local fsmonitor hook, pass `--no-replace-objects` on every identity/cleanliness probe, and verify Git's reported top-level directory is exactly the runner root before treating Git metadata as repository identity. The operator-provisioned path is a trust input, not cryptographic authentication: qualification documentation must identify who provisions it and how that local installation is controlled. Missing, invalid, or mismatched configuration fails closed; no silent fallback to inherited PATH.

This ADR records the accepted trust-source policy; it does not choose a machine-wide installation location, installer, version pin, signature scheme, allowlist service, or administrator-level integrity guarantee. Those details require separate evidence and authorization.

### What this IS NOT

This is not a general host sandbox, Git binary attestation, protection against an OS administrator or equally privileged process, source-tree immutability, mutate-and-restore detection, or authorization for runtime/device/network effects. It does not alter ADR-015/017/018 or the DeviceOps runtime contract.

### Success criteria

- A fake `git` earlier on inherited PATH cannot affect any source identity or untracked-input probe. **Implemented/reviewed** in PR #17 exact head `bfd290f7fa94670c7e745c02ffc93aea7ea731c5`; scoped receipt #6176758662.
- The explicitly selected executable is used consistently for pre-run and post-run probes. **Implemented/reviewed** at the same exact head; repository-local `core.fsmonitor` execution is disabled and sentinel-tested.
- A wrong Git top-level, unavailable executable, malformed selection, or failed probe prevents a SHA-bound receipt. **Implemented/reviewed** at the same exact head; full Issue #81 qualification remains incomplete.
- Replacement refs cannot make identity/cleanliness probes describe a different tree. **Implemented/reviewed** at the same exact head; mismatch fails closed.
- Archive-asserted mode remains explicitly distinct and does not claim Git-authenticated identity. **Implemented/reviewed** at the same exact head; archive SHA remains caller-asserted, not authenticated.

## Consequences

### What gets easier

The runner's source and untracked-input claims have an explicit executable-selection authority, and test evidence can distinguish caller-asserted archive identity from Git-probed repository identity.

### What gets harder

Operators must provision and select Git deliberately; local setup and qualification instructions gain a prerequisite. Selection alone does not prove binary integrity, so the local toolchain trust assumption remains explicit and may differ across hosts.

### What does not change

Only conformance-runner Git probes are in scope. Python selection, manifest cases, evidence classes, receipt privacy, Windows Job Object behavior, production/runtime code, hardware authorization, and the five-path PR #17 scope do not change.

## Alternatives Considered

### Trust inherited PATH

Rejected: the exact-head security review demonstrated that a lower-trust PATH entry can substitute Git and falsify both SHA and untracked-input results.

### Resolve `git` from the current PATH and then pin the resulting absolute path

Rejected: this removes later PATH changes but does not authenticate the initial selection; the attacker-controlled executable may be the one resolved.

### Require an operator-provided absolute executable path

Selected: it makes selection explicit and auditable without creating a new installer or system-wide policy. It still relies on the operator's provisioning and local OS trust; it is not binary attestation.

### Always use archive-asserted mode and omit Git probes

Not selected as the general policy: it avoids Git executable lookup but weakens repository-mode source and untracked-input checks and cannot establish a Git-observed clean source tree. It may remain a bounded mode where its `archive-asserted` limitations are accepted.

## Test Contract

| Claim | Test | Currently |
|---|---|---|
| Only the explicitly configured absolute Git executable is used; inherited executable/config and repository/index selector variables cannot redirect probes | `tests/conformance/test_runner.py::test_git_probe_requires_explicit_absolute_executable`; `test_git_probe_ignores_inherited_path_and_git_overrides` | Implemented and independently reviewed in runner PR #17 exact head `bfd290f7fa94670c7e745c02ffc93aea7ea731c5`; the regression asserts `GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_INDEX_FILE`, and Git config overrides are removed; scoped PASS #6176758662 |
| Local fsmonitor command hooks cannot execute during source probes | `tests/conformance/test_runner.py::test_git_probe_disables_repository_fsmonitor_hook` | Implemented and independently exercised with a temporary repository-local sentinel; scoped PASS #6176758662 |
| Replacement refs cannot alter accepted source identity | `tests/conformance/test_runner.py::test_replacement_refs_fail_closed_before_git_source_identity_is_accepted` | Implemented and independently reviewed; replacement-ref case fails closed, #6176758662 |
| Selected Git top-level must equal runner root and mismatched SHA fails closed | `tests/conformance/test_runner.py::test_source_sha_mismatch_in_git_mode_fails_closed` | Implemented and independently reviewed; overall qualification remains partial |
| Archive mode remains caller-asserted and distinct | `tests/conformance/test_runner.py::test_archive_source_sha_is_asserted_and_git_state_unknown`; `test_archive_skips_git_untracked_scan` | Implemented and independently reviewed; archive identity remains asserted, not authenticated |
| The bounded pytest-influencer scan and pre/post source checks fail closed for covered inputs | `tests/conformance/test_runner.py::test_ignored_conftest_is_detected_even_when_gitignore_excludes_it`; `test_untracked_inputs_changing_during_run_abort_receipt` | Implemented and independently reviewed; scan is limited to documented pytest control-file patterns, not arbitrary filesystem immutability |

These tests establish the named runner behaviors only. They do not qualify the entire Issue #81 validation program, authenticate the Git binary, or prove hardware/runtime behavior.

## Rollback

Owner acceptance of the trust-source decision is recorded in [Issue #81 comment #6175603056](https://github.com/ozand/adv/issues/81#issuecomment-6175603056). The runner correction is implemented and has a scoped independent review at exact PR #17 head `bfd290f7fa94670c7e745c02ffc93aea7ea731c5` (#6176758662). Broader Issue #81 qualification remains partial, with 13 validation rows NOT_RUN and no hardware/service lifecycle qualification. If this decision is later reversed, a superseding ADR should document the replacement trust source; reverting runner code alone would reopen the reviewed false-identity path.

## References

- ADV Issue [#81](https://github.com/ozand/adv/issues/81), current PR #17 security finding [#4266557209](https://github.com/ozand/deviceops/pull/17#discussion_r4266557209)
- ADV ADR-015, ADR-017, ADR-018, ADR-021, and [D01](../deviceops/D01-DECISION.md)
- Prior corrected Python import-path finding [#4266253197](https://github.com/ozand/deviceops/pull/17#discussion_r4266253197)
