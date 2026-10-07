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

The default output is `sources/repo/catalog-candidates.json`. The command resolves
relative output paths from the project root and permits configurable destinations
only beneath the resolved local `sources/repo/` root. Symlink, junction, or
reparse-point redirection outside that root is rejected by the path checks. Tests
exercise directory-symlink escapes where supported and Windows directory-junction
escapes for the output parent, `sources/` root, and `sources/repo/` root; they do not
prove behavior for every Windows reparse-point type. Output creation is
exclusive: an existing destination is left unchanged and the command reports
an error; choose a new
filename rather than relying on implicit refresh/overwrite. These checks protect
against accidental/static path redirection and overwrites; they are not race-safe
against a concurrent untrusted actor changing the local directory tree between
validation and file creation. The workflow assumes the local project directory is
not concurrently mutated by an untrusted actor.
Both the snapshot and output must remain local/ignored; do not put raw catalog data or cloned source content in `kb/`. The candidate inventory groups normalized URL candidates, not verified repository identities. The normalizer preserves each listing FID/name/URL/author and keeps account-only, missing, unsupported-host, or extra-path entries unresolved. Shared URL groups are not proof that listings are one product. The generated `local_id` is a hash of the lowercased owner/repository candidate; it does not establish upstream identity.

### Reconcile a catalog snapshot (read-only)

For an audit, record the relative snapshot path, its SHA-256, capture date, and the exact `scripts/catalog_inventory.py` commit (and blob SHA) used. Treat a pull request's version as a candidate until merged. Run only the normalizer against a copied, immutable JSON snapshot; do not run clone or source-project scripts for reconciliation.

Check that every Cardputer listing row appears exactly once across normalized repository groups and explicit unresolved listings; preserve row identity separately from its FID value. Assert that the total row partition equals `listing_count` and that `repository_candidate_count` equals the number of unique normalized canonical URLs. If the source contract requires unique FIDs, verify that separately; otherwise flag duplicate FID values without discarding or coalescing their distinct listing rows. Report listing-row count and unique URL count separately; do not expect the legacy `catalog-candidates.json` total (423) to match, because it used a different candidate-selection process.

Compare modern normalized output, legacy `sources/repo/catalog-candidates.json`, and `sources/repo/corpus-manifest.json` as separate datasets. Classify matches, unresolved reasons, known pilot URL exclusions, manifest-only fork/hardware-variant records, clone statuses, and unexplained differences. Do not invent FID links for manifest entries that lack them. A candidate omission does not imply the project is absent from the corpus; a manifest relation does not prove which catalog listing it represents.

`failed` records a past clone attempt, not a verified current upstream cause or availability. `deferred-size` and `alias-duplicate` are selection/status records, not proof every other relevant repository was cloned. A pinned manifest commit identifies the captured local revision only; it does not establish upstream freshness. Report missing refresh cadence or unexplained mappings as unknown rather than inferring them.

Keep generated snapshots/candidate output under ignored `sources/repo/` as required above. Sanitized local audit receipts may be kept under ignored `.search/issue5-audit/`; that separate evidence location does not change the CLI output-root policy. Do not publish raw catalog rows, candidate/manifest files, or local audit receipts.

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

## QMD retrieval status and query workflow

Indexing local clones requires a separately named, project-scoped QMD source
collection over an explicit repository/path allowlist, with generated/vendor
exclusions and a local ignored index. Do not add `sources/` to public raw/wiki
collections, run a global QMD update, or treat search results as verified truth
or permission to republish source. Each indexed path must map through a local
manifest to a distinct repository and exact commit. Until that scoped collection
and provenance are verified, QMD coverage is **not demonstrated**; no claim of
complete searchable corpus is made here.

First use `qmd collection list` to confirm which collections are registered in
the selected local index; names below are examples, not a claim that every host
has them configured. Use read-only commands only: `qmd status`, `qmd search
"<terms>" -c <registered-source-collection>`, and `qmd get <qmd://result>`. For
example, if `adv-source` and `adv-source-metadata` are registered:

```sh
qmd search "CalcPuter Cardputer calculator" -c adv-source
qmd search "Cardulator scientific REPL calculator Cardputer" -c adv-source
qmd search "CalcPuter" -c adv-source-metadata
qmd search "Cardulator" -c adv-source-metadata
```

Use the result's repository-local path or `local_id` to locate its entry in the
local `sources/repo/corpus-manifest.json` and record the pinned commit. A QMD
result establishes retrieval of an indexed document path, not that its content
or revision is current, that embeddings exist, or that a project works on
hardware. Keep query output and per-run counts in a sanitized ignored
`.search/issue5-audit/` receipt, not in public docs.

Run `kb-bootstrap validate --dir kb --project-root .` separately from QMD
runtime checks. Validation checks declared KB structure/links/collection
configuration; it does not refresh the index or prove collection registration,
retrieval, embedding, corpus coverage, or source truth. Do not run `qmd update`
or `qmd embed` as part of a read-only audit. If refresh is separately
authorized, record before/after index status and actual search results; freshness
claims require source revision comparison, not just a successful update command.
