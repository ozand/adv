# ADR-009: Add bounded opt-in microphone and tone diagnostics

**Status**: Proposed
**Date**: 2026-10-08
**Authors**: Repository owner and coding assistant
**Supersedes**: None
**Related**: ADR-006 (bounded diagnostic serial JSON); Issue #43

## Context

Issue #2's finite diagnostic runner represents audio as a physical check requiring owner observation; it does not define explicit microphone capture or tone-output operations. Issue #43 records the owner's authorization to prepare a `mic_test` and `tone_test` proposal and confirms headphones are connected. That authorization does not accept this ADR's detailed public contract; owner review is required before acceptance. It does not authorize runtime capture, playback, device/serial access, installation, or flashing.

The pinned M5Unified 0.2.25 source configures Cardputer-Adv microphone input on GPIO46/41/43, I2S0, and speaker output on GPIO42/41/43, I2S1. Microphone enable/disable callbacks configure and power the ES8311; `Mic.end()` waits for capture-task quiescence, clears pending requests, invokes the disable callback, and uninstalls its I2S driver. The ES8311 may produce zero samples for about one second after power-up; this is an estimate, not a guaranteed warm-up duration. A completed `record` request writes exactly the requested sample count, while `isRecording()` may drop before a callback is delivered; callback absence is not completion evidence.

The speaker enable callback selects the ES8311 headphone-drive path but the examined source does not establish headphone-jack sensing or prove that audio routes only to connected headphones. `Speaker.end()` stops the software playback task and invokes the callback, but the Cardputer-Adv disabled callback contains no codec power-down sequence. Therefore codec restoration after tone output is unknown. Software volume limits do not establish sound-pressure level or prove audibility.

### Problem statement

Provide explicit bounded audio diagnostics without silently changing the existing aggregate runner or transporting raw audio.

### Prior art

ADR-006 supplies the existing bounded serial command and volatile-result pattern. It does not define audio operations. The cited M5Unified tag is upstream implementation evidence, not evidence of Cardputer-Adv hardware runtime behavior.

## Decision

The proposed source contract adds two independent, explicitly requested, one-shot operations to the bounded serial command interface:

- `mic_test <ID>` captures a fixed 256 mono `int16_t` sample buffer at 16 kHz after an approximately one-second ES8311 warm-up delay. It returns only bounded integer RMS and peak aggregates, finite state/reason, and cleanup status. The capture buffer is volatile RAM only and is cleared after confirmed microphone-task quiescence. No sample, waveform, or raw audio is emitted or persisted. Zero signal is `INCONCLUSIVE`, not proof of microphone failure. A completed capture and nonzero aggregate are not a hardware PASS unless the owner provides the separately requested acoustic observation.
- `tone_test <ID>` synthesizes only a fixed 440 Hz software tone with at most 100 ms duration and library master volume 8/255. It has no startup behavior and accepts no arbitrary waveform, frequency, or gain input. A completed software playback is not proof that sound was audible; its result remains `INCONCLUSIVE` pending owner observation. The owner must remove headphones from ears/place them aside before any separately authorized physical playback test.

Each operation uses the existing uppercase ASCII run-ID bound (1–12 characters), retains one volatile result per operation for the current boot, returns the cached result for the same ID without repeating the operation, and rejects a different ID once that operation's slot is occupied. Read-only `mic_result <ID>` and `tone_result <ID>` query their respective retained slots. The operations are sequential and refuse to start while the other audio path is active. They do not run from the aggregate `run` command.

The host/device source contract uses fixed bounded JSON fields and reason enums; raw input, samples, and free-form device errors are excluded. Microphone cleanup calls `Mic.end()` outside the capture callback and clears the sample buffer only after the library reports task stopped and no request pending. Speaker cleanup stops playback, restores the prior software volume, and reports codec power/routing state as unknown. A timeout or uncertain cleanup is `INCONCLUSIVE`; no automatic retry is allowed.

If accepted, this decision will extend the diagnostic operation set without changing the four existing ADR-006 commands or their frame contracts. It does not claim that the speaker is safely routed to headphones, that a tone is inaudible with headphones connected, that codec power is restored, that acoustic measurements are calibrated, or that either operation has passed on hardware. It does not authorize runtime execution, serial access, installation, or flashing.

### What this IS

- Two explicit, bounded diagnostic commands that reuse already pinned M5Unified APIs.
- Aggregate-only microphone reporting and a fixed synthesized tone; operation outcomes remain distinct from physical observation.
- A proposed source/API contract for review; Issue #43 separately authorizes source/build work but does not itself accept this ADR.

### What this IS NOT

- Continuous recording, streaming, audio-file handling, arbitrary audio playback, SPL measurement, headphone detection, or a hardware health certification.
- Automatic audio testing at boot or as part of `run`.
- Permission to access a device, COM/serial port, capture/play sound at runtime, install, flash, or modify hardware state outside this source increment.

## Consequences

### What gets easier

The host can explicitly request bounded audio operations and receive sanitized, finite results without transporting raw audio.

### What gets harder

The command parser and host validator must preserve ID, bounds, cache, and uncertainty semantics. Audio operations share hardware resources, and software playback completion does not establish acoustic output or codec power restoration.

### What does not change

ADR-006's existing `status`, `sd_test`, `run`, and `result` contracts remain unchanged. Device/runtime operations still require separate authorization. Audio remains unverified on physical hardware.

## Alternatives Considered

### Include audio implicitly in `run`

Rejected because microphone capture and speaker output are effects that should never occur as a side effect of the existing aggregate runner.

### Return raw audio samples

Rejected because aggregate-only results meet the diagnostic need while minimizing sensitive data and transport exposure.

### Claim PASS from software completion

Rejected because API completion cannot prove microphone acoustic input, speaker audibility, output routing, or hardware function.

### Add jack detection, direct GPIO power control, or codec-register writes

Rejected because the examined pinned source does not establish a safe supported interface for these behaviors; inventing control paths would expand the hardware and trust boundary.

## Test Contract

| Claim | Test | Current evidence |
|---|---|---|
| Only fixed `mic_test`/`tone_test` command forms and bounded IDs are accepted | Source-contract parser tests | Pending implementation |
| Mic result contains aggregates only and never sample bytes | Firmware serializer/source-contract and host schema tests | Pending implementation |
| Mic capture waits for exact completion; timeout remains inconclusive; buffer is wiped only after confirmed quiescence | Source-contract lifecycle tests | Pending implementation; no device runtime test authorized |
| Tone uses fixed synthesis parameters, bounded volume/duration, and never runs at boot | Source-contract tests | Pending implementation; no playback test authorized |
| Conflicting operations are serialized and cached IDs do not rerun | Firmware and host fake-transport contract tests | Pending implementation |
| Existing ADR-006 command/frame behavior is unchanged | Existing regression suite and pinned firmware compile | Pending implementation |
| Codec power/routing uncertainty is not reported as restored or audibly verified | ADR/source review and result-schema tests | Pending implementation; hardware behavior unknown |

Owner acceptance of the detailed bounds, response fields, cache behavior, and cleanup semantics remains pending. Source/build authorization is not acceptance of these design details.

## Rollback

Remove the two audio command handlers, their result state, and the corresponding host schema support while preserving the ADR-006 command handlers and response contracts. No audio data is persisted, so no retained audio artifact requires migration or deletion. Once clients use the new commands, removing them is a public interface break and requires coordinated client retirement.

## References

- [Issue #43](https://github.com/ozand/adv/issues/43), including owner contract confirmation [6070865816](https://github.com/ozand/adv/issues/43#issuecomment-6070865816)
- [ADR-006](ADR-006-hardware-diagnostic-serial-json.md)
- [M5Unified 0.2.25 source tag](https://github.com/m5stack/M5Unified/tree/fd40d58b8405ad1e7ed7afab548dab5e7cec5bbb), especially `src/M5Unified.inl`, `src/utility/Mic_Class.hpp`, and `src/utility/Speaker_Class.hpp`
