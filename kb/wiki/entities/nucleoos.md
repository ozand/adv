---
type: "Project"
title: "NucleoOS"
description: "A source-bounded overview of a Cardputer firmware and browser shell."
issue: "https://github.com/ozand/adv/issues/136"
sources:
  - resource: "https://github.com/indecenti/NucleoOs"
    revision: "8a5c6bea27a73577ba22ddffd7e6ec867e961781"
---

# NucleoOS

## Purpose and applicability

[NucleoOS](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/README.md#L5-L12) is presented by its authors as an ESP32-S3 system with a native Cardputer interface and browser console. The README [claims support](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/README.md#L35-L36) for original Cardputer and ADV. These are `source-reported` claims; board compatibility and runtime behavior were not verified.

## Architecture and dependencies

The project's [architecture overview](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/docs/architecture.md#L14-L31) describes ESP-IDF services, storage, native UI and a browser-based workstation. The README describes [web applications served from SD storage and run in the browser](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/README.md#L185-L190). These are source-reported design descriptions, not proof of complete implementation or performance.

In the pinned firmware entry point, `app_main` contains [storage-mount calls](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/firmware/main/main.c#L392-L433) and [conditionally starts the HTTP server](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/firmware/main/main.c#L595-L633). A separate browser-side [capability lookup](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/web/shell/nucleo-app.js#L192-L202) uses a shell broker when present and otherwise requests the device capability endpoint. These are `code-inspected` static structures, not a verified request/response chain. Startup success, served content, security properties and device behavior remain unknown.

## AI and limitations

The README [describes](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/README.md#L209-L219) on-device, browser-based and externally hosted AI paths. Their exact prerequisites, quality, privacy properties and availability were not tested; offline claims must not be generalized to every AI feature.

The pinned [root license](https://github.com/indecenti/NucleoOs/blob/8a5c6bea27a73577ba22ddffd7e6ec867e961781/LICENSE) is PolyForm Noncommercial 1.0.0. This page contains independent short factual descriptions and links, not code or assets; the license identifier is not a general permission to redistribute upstream material or bundled components.

## Related

- [Bounded research summary](../reports/nucleoos-research.md)
- [Cardputer setup overview](../reports/cardputer-setup.md) — general device context, not NucleoOS setup validation.
