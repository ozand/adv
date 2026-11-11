---
type: "Report"
title: "NucleoOS: bounded source research"
description: "A revision-pinned project overview and relation to existing Cardputer knowledge."
issue: "https://github.com/ozand/adv/issues/136"
---

# NucleoOS: bounded source research

## Question and result

How does NucleoOS divide a Cardputer application between native firmware and a browser interface? The [project entity](../entities/nucleoos.md) records the authors' description and a separately inspected firmware entry point. The inspected code includes storage and HTTP startup calls; it does not establish a functioning end-to-end browser session or device support.

## Sources and scope

Source: [indecenti/NucleoOs](https://github.com/indecenti/NucleoOs) at commit `8a5c6bea27a73577ba22ddffd7e6ec867e961781`. Bounded direct public-file inspection covered [README](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/README.md), [architecture](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/docs/architecture.md), selected lines of [firmware entry point](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/firmware/main/main.c), and a [browser capability lookup](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/web/shell/nucleo-app.js#L192-L202). No source code, screenshots, models or binaries were copied; no build or device test ran. The inspected files were read through pinned public-file responses. A shallow, blob-filtered local clone without checkout was also recorded as a research input; it does not establish complete source or binary availability.

## Relationship to existing knowledge

The [Cardputer setup overview](cardputer-setup.md) provides general device context; it is not a NucleoOS installation or compatibility assessment. The existing [task-oriented navigation](task-oriented-navigation.md) is limited to four approved routes, none covering a browser workstation. A bounded text search of canonical wiki pages for browser/web-interface terms did not identify a suitable existing mechanism page to enrich. This is a limited search, not a claim that none exists anywhere; no route or new reusable concept is inferred from a single source example.

## Open questions and publication boundary

The exact firmware-to-browser request path, app permissions, startup across boards and AI execution prerequisites need further source inspection or separately authorized tests. The upstream [root license](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/LICENSE) identifies PolyForm Noncommercial 1.0.0. This summary and entity use brief independent factual paraphrases and links, not upstream text, code or assets; this is not a general license clearance for reuse. No private paths, captures, credentials or device data are published.
