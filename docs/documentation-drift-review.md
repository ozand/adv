# Documentation and ADR state review (Issue #24)

## Scope and evidence labels

This is a bounded reconciliation report, not an ADR acceptance, a publication-policy change, or a synchronization of the primary checkout. Public GitHub `main` is pinned to merge commit [`5047033`](https://github.com/ozand/adv/commit/5047033d0cf04c5521937c460a52cbf560add4b1) (2026-10-08); its parent is [`4151860`](https://github.com/ozand/adv/commit/4151860c1ef2467abf8b3db599fb6229c49dd194) (2026-10-07). The latter was the published base reviewed during the original drift investigation. The primary checkout observed then had HEAD `074d623e8f9ec168b91dbaf639946d52ca99bba9`, with tracked README/AGENTS/ADR edits and untracked ADR drafts; those local files are not treated as published evidence here.

Evidence labels used below:
- **Published:** content or history directly present in a pinned public commit.
- **Recorded report:** a GitHub issue comment reports a decision or state; this proves the report was recorded, not independent human-turn provenance.
- **Not found:** no matching public evidence was located in the bounded review; this is not proof that no decision exists elsewhere.
- **Unresolved:** evidence conflicts or does not establish the intended current policy.

## Published ADR state at the reviewed base

At `4151860c1ef2467abf8b3db599fb6229c49dd194`, the published blobs were README `817fd0900d41323b0b171418bc4c23b5c309d59d`, AGENTS `d19988c7eb043bbb6a6b952c84f09df11d556af7`, ADR-001 `d8999970b408fbf2e0d1863c2d493754e5e9ac18`, and ADR index `b9b8b4555c312e566f9163345a6f38f45cf34ad7`. The index lists ADR-001, ADR-004, and ADR-006 as Accepted. ADR-002, ADR-003, and ADR-005 are absent from that published index and their corresponding ADR files are absent from the pinned public tree. The current `main` after the privacy-only PR #25 retains this ADR status/index state; PR #25 changed only README and ADR-001 wording.

| Decision | Public evidence and provenance | Reconciliation status |
|---|---|---|
| ADR-001 — separate public synthesized knowledge | Published at the pinned base; privacy wording was narrowly redacted by PR #25, merged as `5047033d0cf04c5521937c460a52cbf560add4b1`. | Accepted status unchanged. The redaction does not alter the decision or resolve capture policy. |
| ADR-002 — reviewed research captures | Owner-account Issue #3 comments [6026992432](https://github.com/ozand/adv/issues/3#issuecomment-6026992432) (2026-10-06 22:59:25Z) and [6027073391](https://github.com/ozand/adv/issues/3#issuecomment-6027073391) (23:06:15Z) record approval to track reviewed, machine-readable `kb/research/` captures. Later Issue #5 comments [6030358978](https://github.com/ozand/adv/issues/5#issuecomment-6030358978) (2026-10-07 03:35:27Z) and [6030933984](https://github.com/ozand/adv/issues/5#issuecomment-6030933984) (04:28:11Z) report ADR-002 superseded by ADR-005. The ADR file is absent from reviewed public main. | Recorded reports exist; no ADR-002 file/index publication in reviewed main. Do not restore or mark supersession in the public index from local draft alone. |
| ADR-003 — local QMD source collection | Issue #5 comment [6027855988](https://github.com/ozand/adv/issues/5#issuecomment-6027855988) (2026-10-07 00:07:43Z) records approval; follow-up [6028342661](https://github.com/ozand/adv/issues/5#issuecomment-6028342661) (00:45:06Z) reports design acceptance and partial implementation. Both are account-authored issue records, not independent proof of the originating human turn. ADR-003 is absent from reviewed public main. | Recorded approval report exists; public ADR publication is absent. Do not infer public Accepted status from a local draft. |
| ADR-004 — ignored local lessons | Public ADR-004 is present as Accepted in the reviewed index. Issue #7 comment [6033835561](https://github.com/ozand/adv/issues/7#issuecomment-6033835561) (2026-10-07 08:13:32Z) records explicit acceptance; public PR #9 history records proposed status at review followed by an acceptance update. | Published Accepted status is consistent with later recorded acceptance. No correction needed. |
| ADR-005 — local catalog repositories | Issue #5 comments [6030358978](https://github.com/ozand/adv/issues/5#issuecomment-6030358978) and [6030933984](https://github.com/ozand/adv/issues/5#issuecomment-6030933984) report ADR-005 accepted and ADR-002 superseded. ADR-005 is absent from the reviewed public index/tree. | Recorded decision report exists; publication gap remains. Do not promote the local draft or change index status without a separately reviewed publication decision. |
| ADR-006 — bounded serial JSON diagnostic status | Present as Accepted in the published ADR index at `4151860`; Issue #2 PR #23 commit records the accepted ADR in its public delivery rationale. | Published Accepted. Not part of the older local ADR-001..005 drafts; do not renumber or rewrite it here. |

## Causal timeline and documentation observations

- Public main advanced from the primary checkout’s observed `074d623` to `4151860` through subsequent reviewed work. The primary also had dirty and untracked documentation at discovery. This establishes divergence, not the authorship or exact copy-forward cause of every local sentence.
- PR #9 initially reviewed ADR-004 as Proposed; subsequent public issue/commit records changed it to Accepted. The published state is therefore not contradicted by the earlier proposal.
- The reviewed public README and ADR-001 previously contained a private local-network locator. PR #25 removed two occurrences from those two public files; it did not rewrite history. Current wording intentionally omits private local-network details.
- The local KB index was reported to contain a stale sentence claiming no canonical entities while listing two entity paths. This report does not promote that local observation into a published-main claim; its exact tracking/publication state was not established here.
- A retained dated QMD receipt reports a project-root refresh that listed four collections (`adv-research`, `adv-source`, `adv-source-metadata`, `adv-books`) and snapshot counts before/after. These are historical run observations, not current index health or byte-integrity proof. QMD declarations and runtime registrations are distinct; no QMD command was run for this report.
- An earlier command record used a timeout argument of `600000` while actual elapsed time was about 14m48s. Treat this as a historical command/protocol mismatch, not evidence that a current process or index is healthy or corrupt.

## Unresolved publication-policy question

Issue #3 comments 6026992432/6027073391 record owner-account approval for publishing reviewed machine-readable `kb/research/` captures. The overview wording and other published guidance describe source captures/material as local-only and public knowledge as synthesized content. The difference is unresolved here. This report makes no choice between those statements, does not change ADR-001/002/005 status, and does not authorize publication of any raw capture.

## Bounded next steps

1. Preserve the distinction between public `main` and the primary checkout’s dirty/untracked WIP; do not bulk-copy local ADR drafts or rewrite history.
2. Obtain an explicit owner policy decision on the reviewed-capture publication boundary before changing the governing public guidance or ADR status.
3. Separately verify the exact local KB-index claim and local QMD receipt provenance before proposing factual local-only reconciliation; do not run QMD or publish private receipts as part of this report.
4. Review ADR-003/005 publication status and owner-reported acceptance evidence as a separate governance step; this report alone does not mark absent ADRs Accepted.

No device/hardware test, live metadata request, source-project clone, QMD operation, test/build, or private source retrieval was performed for this report. The clean repository checkout used to prepare this documentation-only change contains no source-project corpus.
