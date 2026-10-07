# Local Cardputer catalog corpus (Issue #5)

This workflow treats Launcher entries as listings, not verified projects. It
keeps listing IDs and names while grouping candidate GitHub owner/repository
URLs. Account-only, missing, and non-GitHub URLs remain explicit unresolved
records; canonical identity, fork lineage, relevance, default branch, and
revision must be verified before cloning or drawing conclusions.

## Build candidate inventory

Save the public response from `https://api.launcherhub.net/giveMeTheList` as a
local JSON file outside tracked KB directories. Then run from the repository
root:

```sh
python scripts/catalog_inventory.py /path/to/launcher-catalog.json
```

The default output is `sources/repo/catalog-candidates.json`. Both the snapshot
and output must remain local/ignored; do not put raw catalog data or cloned
source content in `kb/`. The candidate inventory is a reproducible URL
normalization, not an assertion that every URL is a repository or that multiple
listings are one product. URLs with extra path segments are unresolved until
verified as repository roots. The local directory ID preserves the owner/repo
separator to prevent collisions between different owner/repository pairs.

## Clone and refresh safeguards

Clone only public, relevant Git repositories. Use shallow/no-tag clones and
record each catalog FID/name, original and canonical URL (including redirects),
default branch, exact commit, clone result/failure, and any size/time cap in a
local manifest next to the clones. Preserve fork/derivative identity as separate
projects. Do not overwrite an existing directory during refresh; inspect its
identity and revision first. Record unavailable, oversized, unsafe, irrelevant,
and failed candidates with reasons. Never stage or publish `sources/`.

Set finite per-repository and total time/size limits before a batch; stop rather
than expanding limits automatically. Exclude binaries, generated/build output,
vendored dependencies, and irrelevant Markdown from retrieval. Firmware claims
must cite exact board definitions and distinguish generic ESP32-S3 support from
Cardputer-Adv board/peripheral support and installed-device state. This workflow
does not authorize device operation.

## QMD retrieval status

Indexing local clones requires a separately named, project-scoped QMD source
collection over an explicit repository/path allowlist, with generated/vendor
exclusions and a local ignored index. Do not add `sources/` to public raw/wiki
collections, run a global QMD update, or treat search results as verified truth
or permission to republish source. Each indexed path must map through a local
manifest to a distinct repository and exact commit. Until that scoped collection
and provenance are verified, QMD coverage is **not demonstrated**; no claim of
complete searchable corpus is made here.
