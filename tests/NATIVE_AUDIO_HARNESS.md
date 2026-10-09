# Issue #43 native harness (bounded extracted-code verification)

Target firmware source: `scripts/hardware_check/hardware_check.ino` at commit `de59f24ac5032e968b6725d7f7ea212937a20f17` (Git blob `88e0aaf6abbd5fed579c095e2228d595a3341206`; source SHA-256 `4211cc94bd51e85348069107cd685e351bbce4cd0c26e514c56dd57e549b8bed`).

`native_audio_harness.cpp` is a source-derived harness: it includes extracted firmware definitions for `audioReasonAllowed`, `audioResultPairValid`, `validRunId`, `emitAudioJson`, and the four audio-command branches from `handleCommandLine`. Hardware-facing `M5` and serial behavior are replaced by small stubs; `executeMicTest`/`executeToneTest` increment counters and set deterministic cached values. Its main compares hard-coded compact expected mic, tone, and generic-error byte frames against the extracted emitter (including CRLF and field order), checks the 256-byte cap, checks partial-write fail-stop, and exercises mic replay `mic_test A1 -> mic_result ZZ -> mic_test B2 -> mic_result A1` preserving exact response bytes with one executor call. It does not compile the complete firmware source, and extraction correspondence must be checked against the pinned target source when the excerpt changes.

## Execution receipt

Executed 2026-10-09 in a Windows x86_64 MSYS2 shell using portable w64devkit v2.10.0 / GCC 16.2.0 (GCC binary reports `g++.exe (GCC) 16.2.0`). The official GitHub release asset SHA-256 was `18d0a4c71a166f8401ab6305781bec5882b40b5e06ba9807c61cb5f3b3c6325e`; it was extracted selectively inside this scratch directory. No global installation or persistent PATH change was made.

Compile argv: `g++ -std=c++17 -Wall -Wextra -Wpedantic -Werror -O0 native_audio_harness.cpp -o native_audio_harness.exe`; compile exit 0. Executed `native_audio_harness.exe`; exit 0, no stdout/stderr. This execution receipt applies to the frozen harness source with SHA-256 `0f3eb6524d9483d620749591e786b3133a452ca73544de42ce8793c041cb8968`; this tracked file is byte-identical to that executed source. The scratch executable SHA-256 was `8533eb0782a3bda1bf67b52c360722973e852457b733c79827bbed1b03b724f7`.

## Limits

The recorded execution proves only the bounded harness assertions: exact extracted emitter byte frames for one maximum-ID/max-metric mic response, one tone response, one generic error; CRLF and 256-byte cap for that mic frame; partial-write fail-stop; and an adapted audio-branch cache replay sequence `mic_test A1 -> mic_result ZZ -> mic_test B2 -> mic_result A1`, where original bytes are preserved and the stub executor count stays one. The four audio command branches were extracted from source and wrapped; setup and non-audio parser branches were not executed. M5/audio executor APIs are stubs. This is not a full sketch compile, native execution of the complete firmware parser/state machine, audio lifecycle test, exhaustive 29-frame C++ matrix, firmware build, or physical-device evidence.
