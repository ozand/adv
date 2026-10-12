# ADR-014: DeviceOps service-centered agent infrastructure

**Status:** Proposed — подробная архитектура ожидает review/принятия.
**Date:** 2026-10-12.
**Issue:** [#66](https://github.com/ozand/adv/issues/66); документация [#67](https://github.com/ozand/adv/issues/67); решение деталей [#68](https://github.com/ozand/adv/issues/68).
**Supersedes:** None.
**Related:** ADR-006, ADR-007, ADR-009, ADR-013; issues #33–#38.

## Context

Нужна общая инфраструктура, через которую локальные агенты и агенты из вебчата могут диагностировать, настраивать и обслуживать ESP32. ESP Web Tools исследовался как пример браузерной установки и полезных подходов, а не как обязательный центр будущей системы.

12 октября 2026 года владелец в координационном чате явно согласился с направлением «центром должен стать DeviceOps-сервис, а не браузерный прошивальщик» и поручил создать issues и документы в `ozand/adv`. Эта запись отражена в epic #66. Подтверждение относится к направлению и данной документационной поставке; оно не является принятием ещё не рассмотренных схем, runtime stack, trust model или разрешением на hardware/network операции.

Существующие ADR-006/009 задают узкие source-контракты диагностики, а #37 — лишь draft общих operation semantics. Публичный `adv` остаётся базой знаний по ADR-007. Исторические решения не переписываются этим ADR.

## Proposed decision

Спроектировать DeviceOps как общий слой именованных операций с bounded inputs/outputs, target identity, явными эффектами, policy, immutable plans, долговечными заданиями и проверяемым evidence.

Первый путь — host-side core/executor, один владелец устройства, ограниченный serial adapter ADV и семантически одинаковые CLI/MCP. Браузер, vendor-specific tunnel, device-side MCP и OTA не обязательны для локального MVP.

ESP Web Tools остаётся необязательным операторским интерфейсом установки/восстановления; его manifest может строиться из общего каталога артефактов. Он не заменяет DeviceOps authorization, job lifecycle и совместимость. Skills описывают порядок работы через доступные инструменты, но не предоставляют полномочия сами по себе.

Подробный дизайн: [DeviceOps index](../deviceops/README.md), [architecture](../deviceops/ARCHITECTURE.md), [contracts](../deviceops/CONTRACTS.md), [security](../deviceops/SECURITY.md), [deployment](../deviceops/DEPLOYMENT.md).

## Invariants to preserve

Один semantic API для клиентов; transport не расширяет права. ACK, выполнение, проверка firmware и физический PASS различаются. Таймаут/partial write/reset не дают права на blind retry. Grant связан с точным target/operation/plan/artifact и выдаётся доверенной стороной. Lease expiry не считается прекращением старого I/O. Firmware ABI ADR-006/009 сохраняется; их принятие не является аппаратным допуском.

Документы и координация находятся в `adv`. Место кода постоянного сервиса/бинарников определяется D01 с владельцем; отдельный runtime-репозиторий предпочтителен, но ещё не создан и не назван. Никакого неявного изменения publication boundary.

## Alternatives considered

| Вариант | Причина не выбирать центром |
|---|---|
| Автоматизация DOM-кнопок ESP Web Tools | Интерактивный UI не даёт общего contract/policy/durable execution для локальных агентов |
| Прямой raw serial/shell каждой модели | Дублирует семантику, допускает конкуренцию и не обеспечивает bounded effects |
| Только MCP в firmware | Зависит от сети/успешной загрузки приложения; не независимый recovery-путь |
| Облачная платформа с fleet management сразу | Увеличивает объём до проверки одного локального сценария |
| Использовать SDK/MCP tooling без общего core | Полезный reuse, но не решает target binding, grants, jobs и evidence между транспортами |

## Consequences

Появляется единая модель операций и возможность подключать несколько инструментов без переписывания device protocols. Цена — явная обработка неизвестного исхода, сохранение состояния, интеграционные fixtures и security review. Обещание «агент всё сделает сам» заменяется проверяемыми ограниченными режимами автоматизации.

Не следует переписывать esptool, ESP-IDF и тестовые фреймворки. Их версии и безопасные точки интеграции выбираются отдельно. Firmware language и host language не обязаны совпадать.

## Acceptance and test contract

Для принятия подробного решения D01 фиксирует место кода, runtime/OS/IPC/storage, минимальные зависимости и границы доверия; D02/D03 принимают соответствующие схемы/enforcement решения. Owner receipt и независимый review добавляются только после реального выполнения, с exact candidate SHA. В этой версии таких подтверждений не заявлено.

Проверки: [VALIDATION](../deviceops/VALIDATION.md), особенно V01–V12 для local MVP и V13–V20 для deployment/remote. Сначала fake-only; hardware, account/network setup и deployment допускаются отдельно. Публикация/merge этого документа не выдаёт такие права.

## Rollback / evolution

До принятия уточнять proposal через issue/PR. После принятия существенные изменения оформлять новым ADR, сохраняя историю. Отключение optional frontend не должно разрушать локальный core; отключение DeviceOps не изменяет автоматически прошивку устройства и не повторяет незавершённые команды.

## References

[PRD](../deviceops/PRD.md), [roadmap](../deviceops/ROADMAP.md), [evidence sources](../deviceops/REFERENCES.md), [ADR-006](ADR-006-hardware-diagnostic-serial-json.md), [ADR-009](ADR-009-bounded-opt-in-audio-diagnostics.md), [ADR-007](ADR-007-publish-reviewed-research-captures-exclude-local-source-originals.md), [ADR-013](ADR-013-define-bounded-batch-knowledge-workflow.md).
