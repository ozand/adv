# Cardputer knowledge model contract

**Status:** Accepted by the owner as the finite knowledge/evidence contract in ADR-010; acceptance recorded at [Issue #45 comment 6072992191](https://github.com/ozand/adv/issues/45#issuecomment-6072992191). This records the accepted contract, not implementation or enforcement. It does not authorize migration, publication-boundary changes, QMD/index changes, or device verification.

## Compatibility

- Preserve OKF v0.2 `type` as a required nonempty string; its values remain extensible.
- Optional `object_profile` is a consumer classification, not a replacement for universal OKF `type`.
- Unknown metadata remains allowed; no new field is required on existing cards.
- Evidence, applicability, and lifecycle are independent dimensions.

## Candidate metadata

For new or revised canonical cards, retain OKF-required `type`. Recommend `title` as an adv canonical-card requirement (this is stricter than OKF's universal minimum). This proposal recommends the following compact fields; it does not require migration of existing cards:

| Field | Recommendation | Missing/not applicable |
|---|---|---|
| `issue` | Governing issue URI for the authored card | Omit only when no governing issue exists |
| `object_profile` | Optional consumer-facing profile distinct from `type` | Omit when not useful; do not infer from `type` |
| `sources` | Claim-linked source URI, repository/document locator, full revision when available | Mark unavailable revision as unknown; do not invent a pin |
| `evidence` | Per-claim source/method records, using the evidence classes below | Unknown when no qualifying evidence exists; no document-wide grade |
| `applicability` | Per-claim target context when applicability affects interpretation | `unknown` if evidence is missing; `not-applicable` only with an explicit reason |
| `status` | Editorial lifecycle only | Follow current repository convention; never use as evidence strength |

This is the finite metadata recommendation accepted for adv canonical cards. `type` remains the OKF universal required field; `title` is an adv-specific recommendation. No existing-card migration or contract enforcement is authorized by this acceptance.

## Claim-level evidence

Evidence attaches to each claim/source, not a document-wide grade. Mixed cards may separately record `source-reported`, `code-inspected`, and `device-observed` evidence. A README statement is source-reported, not device-verified. Preserve source identity (repository/document and full revision when available); missing details remain unknown.

`device-verified` is a distinct, higher-threshold claim class. It requires a claim-bounded direct observation tied to exact device model, installed firmware/software revision and relevant configuration; documented procedure; observed result; source/provenance; and limitations. A `device-observed` record is the underlying observation, not automatic verification of behavior or other claims/capabilities. Record verifier/confirmation context. If identity, revision, procedure, or result is unresolved, the claim is not device-verified. No device verification was performed for this proposal.

Evidence fields and meanings above are the finite accepted contract. Structural presence proves neither claim truth nor runtime behavior.

## Applicability and lifecycle

Applicability is target context, not confidence. Candidate states:
- `applicable`: evidence supports stated target/version;
- `not-applicable`: explicitly outside claim target scope;
- `unsupported`: evidence explicitly establishes lack of support;
- `unknown`: target/version evidence missing or ambiguous.

Missing version/test means unknown, not unsupported; not-applicable differs from unsupported. Lifecycle status is editorial (draft/stable/deprecated). Stable does not mean source-verified, code-inspected, or device-tested.

## Existing knowledge layers

- `kb/raw/`, `kb/research/`: bounded evidence after ADR-007 privacy, secrets, relevance, provenance and rights review.
- `kb/wiki/`: canonical synthesis; summarizing does not upgrade source evidence.
- `sources/`: ignored original repositories, books, binaries, private/bulky sources; never publish originals.
- `local-lessons/`: optional ignored operational lessons under ADR-004, separate from canonical public KB.
- QMD/index membership is retrieval state, not evidence quality or publication permission.

This proposal preserves these boundaries and adds no layer.

## Invalid inferences

- stable therefore device-verified;
- README feature statement therefore installed Cardputer support;
- missing firmware version therefore unsupported;
- object_profile replaces required OKF type;
- one evidence grade covers claims from different methods/sources;
- QMD/index presence proves a claim or permits publication.

## Owner decisions before adoption

Future changes to vocabularies, required fields, claim-reference representation, applicability semantics, or evidence-review requirements need separate owner decision. Existing-card migration, enforcement, QMD operations, and device observation are not authorized by ADR-010 acceptance. Structural validation, evidence review, factual verification, rights/privacy review, and device observation remain distinct checks.
