---
type: "Concept"
title: "WPAD-related source structures"
description: "A bounded source-inspected example of proxy configuration and DHCP option construction, not a verified operation."
issue: "https://github.com/ozand/adv/issues/100"
sources:
  - resource: "https://github.com/7h30th3r0n3/evil-m5core2"
    revision: "45928e0312a0f897a4329003033c3714f839bd6d"
evidence:
  - claim: "The source defines proxy auto-configuration text and separately constructs DHCP option 252 containing a configuration URL."
    source: "https://github.com/7h30th3r0n3/evil-m5core2/blob/45928e0312a0f897a4329003033c3714f839bd6d/awok/awok.ino"
    revision: "45928e0312a0f897a4329003033c3714f839bd6d"
    method: "code-inspected"
    locator: "lines 4964–4977 and 17576–17582"
---

# WPAD-related source structures

At the pinned revision of `evil-m5core2`, the [source](https://github.com/7h30th3r0n3/evil-m5core2/blob/45928e0312a0f897a4329003033c3714f839bd6d/awok/awok.ino#L4964-L4977) defines proxy auto-configuration text. A separate [packet-construction section](https://github.com/7h30th3r0n3/evil-m5core2/blob/45928e0312a0f897a4329003033c3714f839bd6d/awok/awok.ino#L17576-L17582) writes a configuration URL into DHCP option 252. These are static source structures, not an observed exchange.

## Evidence and limits

| Relation | Evidence and status |
|---|---|
| Source | Pinned `evil-m5core2` source; two separate sections inspected. |
| Operation | Static configuration text and option construction: `code-inspected`; their connection and delivery to a client: `unknown`. |
| Device | Cardputer applicability and compatibility: `unknown`; the source name does not establish support. |
| Output and effects | Actual proxy selection, client behavior, network effects and runtime correctness: `unknown`. |
| Verification | No firmware execution, device or network test. |

The source is outside the report's 46 candidate rows; its eligibility is unresolved and this example establishes no coverage denominator. No configuration values or deployment instructions are reproduced.

## Related

- [Portal request structure](wifi-evil-portal-structure.md)
- [Partial Wi-Fi domain synthesis](../../reports/protocols/wifi.md)
- [Issue #100](https://github.com/ozand/adv/issues/100)
