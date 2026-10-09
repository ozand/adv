---
type: "SetupGuide"
title: "Getting started with M5Stack Cardputer"
description: "Identify Cardputer versus Cardputer-Adv, prepare for a documented development route, and find the official model-specific tutorials without implying installation or firmware verification."
tags: [cardputer, setup, getting-started, m5stack]
status: stable
issue: "https://github.com/ozand/adv/issues/1"
sources:
  - resource: "https://docs.m5stack.com/en/core/Cardputer"
    revision: "Official product documentation, accessed 2026-10-09; mutable page"
  - resource: "https://docs.m5stack.com/en/core/Cardputer-Adv"
    revision: "Official product documentation, accessed 2026-10-09; mutable page"
  - resource: "https://github.com/m5stack/M5Cardputer-UserDemo/blob/a34d7ebcd508fb903a2b1123be8c8b54abd55d07/README.md"
    revision: "a34d7ebcd508fb903a2b1123be8c8b54abd55d07"
    document: "README.md"
  - resource: "https://github.com/m5stack/M5Cardputer-UserDemo/blob/b549eac0a3c65bc108186c276b8fac0a214aaa4e/README.md"
    revision: "b549eac0a3c65bc108186c276b8fac0a214aaa4e"
    document: "README.md"
---

# Getting started with M5Stack Cardputer

This guide helps you identify which Cardputer model you have and choose an official starting point. Product details and tool versions below are manufacturer/upstream documentation, not a check of your device. No device was connected, installed, built, or flashed for this guide.

## 1. Identify the model first

- **Cardputer (K132)** uses the Stamp-S3 core module. M5Stack lists a 56-key keyboard, 1.14-inch display, microphone, speaker, IR emitter, Grove connector, microSD slot, and Arduino IDE, UiFlow2, ESP-IDF, and PlatformIO as development platforms.
- **Cardputer-Adv (K132-Adv)** uses Stamp-S3A. Its documented hardware differs, including a BMI270 motion sensor, EXT 2.54-14P expansion bus, ES8311 audio codec, headphone output, and 1750 mAh battery. Do not assume tutorials, pins, peripherals, or firmware for one model apply to the other.

Check the model/SKU printed on the device or packaging and compare with the official [Cardputer](https://docs.m5stack.com/en/core/Cardputer) and [Cardputer-Adv](https://docs.m5stack.com/en/core/Cardputer-Adv) pages. If identification is uncertain, stop before selecting firmware or board-specific examples.

## 2. Choose a documented first route

For a first interactive experiment without setting up a native build toolchain, use the model's official UiFlow2 tutorial linked from its product page. For code-based development, use that page's Arduino IDE tutorial and model-specific Arduino library/driver links. M5Stack also lists ESP-IDF and PlatformIO, but the precise toolchain depends on the project you choose.

The official hardware-evaluation [UserDemo README](https://github.com/m5stack/M5Cardputer-UserDemo/blob/a34d7ebcd508fb903a2b1123be8c8b54abd55d07/README.md) specifies ESP-IDF v4.4.6 and explicitly directs Cardputer-ADV users to its separate `CardputerADV` branch. That branch's [README at commit `b549eac`](https://github.com/m5stack/M5Cardputer-UserDemo/blob/b549eac0a3c65bc108186c276b8fac0a214aaa4e/README.md) specifies ESP-IDF v5.4.2 and describes fetching dependencies before building. These are instructions for that source project—not a universal toolchain recommendation or proof that a build will succeed on your host.

Before following a project tutorial, confirm its model/branch, required software version, USB data-capable cable, and host OS from that tutorial. Keep credentials and private configuration out of public files and source control.

## 3. Keep first steps non-destructive

Read the model-specific quick start before connecting hardware or changing software. This guide does not require entering download mode, restoring factory firmware, erasing flash, or opening the device. M5Stack documents download-mode button sequences, but this guide has not exercised them; entering that mode is not the same as installing firmware.

Firmware flashing, factory restore, flash erase, and advanced module repair can alter or erase device data. They are outside ordinary setup here: do not perform them without separate explicit authorization, a verified model-specific procedure, and a recovery plan. If a device is not recognized or a tutorial does not match the exact model, stop and consult the vendor's current support documentation rather than trying a different model's image or pinout.

## 4. What this guide does not establish

The documentation describes product capabilities and project instructions. It does not establish which firmware is installed on your unit, whether a particular build works with your toolchain, or whether hardware features operate correctly. Those remain unknown until separately and safely verified.

## Sources and evidence limits

- M5Stack [Cardputer product documentation](https://docs.m5stack.com/en/core/Cardputer) and [Cardputer-Adv product documentation](https://docs.m5stack.com/en/core/Cardputer-Adv), accessed 2026-10-09. The live documentation is mutable; no immutable page revision was available.
- M5Stack [UserDemo main README](https://github.com/m5stack/M5Cardputer-UserDemo/blob/a34d7ebcd508fb903a2b1123be8c8b54abd55d07/README.md) and [CardputerADV README](https://github.com/m5stack/M5Cardputer-UserDemo/blob/b549eac0a3c65bc108186c276b8fac0a214aaa4e/README.md), each pinned to the cited commit.
- The ADV branch's root `LICENSE` was not present at the pinned revision; this guide reproduces no source code, images, or extended source text. No license conclusion is made for that branch.
