# Project QMD usage

QMD searches Markdown in a locally selected index and its registered collections. For this repository, distinguish the ignored project-local runtime index from the parent workspace index and from tracked declarations under `qmd/collections/`. A declaration is not proof that a collection is registered in the active index. A clean clone may have no project-local index or registered source collections.

## Select and inspect the runtime index

Run commands from the repository root (`ozand/adv`). First inspect `qmd status` and `qmd collection list` without changing state. Confirm the reported index is the intended project-local runtime index before searching. If it instead selects a parent/workspace or otherwise unexpected index, stop; do not redirect or modify it as part of routine lookup. The optional `--index` argument selects an index database, not a collection; use it only when its target is explicitly configured and approved. Do not hard-code a user home path or assume a fresh clone has the same registrations.

## Read-only lookup

Use only collections shown by `qmd collection list` for the selected index. The following names are examples observed in a dated local receipt, not guarantees of current registration or health:

- `adv-source` — local source-document collection
- `adv-source-metadata` — local manifest/candidate metadata collection
- `adv-research` and `adv-books` — other observed local collections

Example commands (only if each collection is listed in the active index):

```sh
qmd search "Cardputer display driver ST7789" -c adv-source
qmd search "CalcPuter" -c adv-source-metadata
qmd get qmd://adv-source/<result-path>
```

A result shows that QMD returned an indexed document reference; it does not prove the bytes match an upstream revision, that the source is current, that a vector exists, that a query will work offline, or that the project works on hardware. Follow repository-local manifest provenance where available and treat absent revision evidence as unknown. Do not promote search output directly to canonical `kb/wiki/` claims without source review.

## Safety and limits

QMD collection declarations, runtime registrations, Git tracking, and public publication are separate concerns. Under ADR-007, only bounded research captures in `kb/raw/` or `kb/research/` that pass privacy, secret, relevance, provenance, and rights review may be published. Original repositories, whole books/PDFs, binaries, private captures, and bulky source originals remain local-only in ignored `sources/`. QMD indexing is not publication permission.

Do not run `qmd update`, `qmd embed`, `qmd collection add`, or any global refresh/registration command as part of lookup. Those operations mutate local index/configuration state and require a separately scoped authorization and verified target index. This guide does not authorize them.

Historical receipts record zero embedded vectors and a prior update reporting four collections; these are dated observations, not assertions about current index state, freshness, completeness, or offline availability. A prior subprocess-status-code issue remains unresolved: never report lookup success solely because a wrapper returned success if the QMD process result was not verified. If status propagation is unclear, report the QMD result as unknown and stop rather than retrying or mutating the index.
