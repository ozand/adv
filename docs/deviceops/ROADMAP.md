# DeviceOps — задачи и порядок выполнения

**Дата плана:** 2026-10-12. **Epic:** [#66](https://github.com/ozand/adv/issues/66). Состояние выполнения проверять в issues/PR: таблица ниже описывает зависимости, а не автоматически обновляемый dashboard.

## 1. Backlog локальных агентов

| ID / Issue | Результат | Основные зависимости / gate |
|---|---|---|
| D00 / [#67](https://github.com/ozand/adv/issues/67) | Этот пакет требований, архитектуры и задач | Поручение владельца; reviewed PR |
| D01 / [#68](https://github.com/ozand/adv/issues/68) | Owner-accepted choices: Python/Windows, persistent executor/named-pipe IPC, SQLite, private runtime repo/path. Qualification, dependency review and #37/#38 inputs remain open | D00; [D01 decision record](D01-DECISION.md), Accepted ADR-015–017; remaining qualification is separately scoped |
| D02 / [#69](https://github.com/ozand/adv/issues/69) | Схемы операций и golden/negative fixtures | D01 для принятия; draft параллельно |
| D03 / [#70](https://github.com/ozand/adv/issues/70) | Identity, policy и привязанные grants | D01/D02; threat model параллельно |
| D04 / [#71](https://github.com/ozand/adv/issues/71) | Executor, job store, single writer, restart/reconciliation | D01–D03 |
| D05 / [#72](https://github.com/ozand/adv/issues/72) | Адаптер существующей диагностики ADV | D02–D04; ADR-006/009; без изменения firmware |
| D06 / [#73](https://github.com/ozand/adv/issues/73) | CLI и MCP к одному core | D02–D04; D05 для диагностического parity |
| D07 / [#74](https://github.com/ozand/adv/issues/74) | Каталог артефактов и deploy_plan без записи | D01–D03 |
| D08 / [#75](https://github.com/ozand/adv/issues/75) | Deployment executor и post-boot verification | D04/D05/D07; сначала fake tests |
| D09 / [#76](https://github.com/ozand/adv/issues/76) | Защищённый путь вебчата к локальному executor | D03/D04/D06; account/network setup отдельно |
| D10 / [#77](https://github.com/ozand/adv/issues/77) | Проверенные Skills диагностики и deployment | Diagnose: D05/D06; plan: D07; execute: D08; remote: D09 |
| D11 / [#78](https://github.com/ozand/adv/issues/78) | Optional browser bridge + операторский EWT | D03/D04/D06/D07/D09; browser flash отдельно после D08 |
| D12 / [#79](https://github.com/ozand/adv/issues/79) | Config plan/apply | D01–D04 и принятый реальный firmware profile |
| D13 / [#80](https://github.com/ozand/adv/issues/80) | OTA adapter / confirmation / rollback | D04/D07/D08 и реализованный OTA profile |
| D14 / [#81](https://github.com/ozand/adv/issues/81) | Conformance, клиентская и аппаратная квалификация | План после D02/D03; отдельные slices после их компонентов |

Все задачи содержат входы, deliverables, acceptance criteria, проверки, handoff и границы полномочий. Создание issue не означает, что агент уже назначен или начал её исполнять.

## 2. Критический путь первого результата

```text
D00 documentation
  -> D01 decisions
  -> D02 contracts
  -> D03 policy
  -> D04 executor
  -> D05 diagnostic adapter + D06 CLI/MCP
  -> D14 offline diagnostic slice
  -> separately authorized minimal hardware session
```

D05 и D06 разрабатываются параллельно через согласованные mock interfaces, затем соединяются в parity test. D14-план начинается раньше реализации, а не ждёт окончания всей программы. D14 аппаратный gate не является зависимостью для написания D08/D13 fake-tested кода.

Для первого вебчат-сценария: добавить D09 к прошедшему offline baseline, проверить настоящий клиент на fake device и только затем отдельно разрешённую плату. Браузерный мост не обязателен: вебчат может обращаться к постоянному host executor.

## 3. Параллельные потоки

Во время D01 можно готовить проекты схем D02, threat model D03 и test cases D14. Публичный контракт и enforcement-код не принимаются до согласования связанных ADR; это не запрет на draft-работу.

После D02/D03 независимы core D04 и артефакты D07. После core независимы диагностический adapter/frontend и подготовка config profile. После CLI/MCP возможны remote D09 и диагностический Skill D10. Deployment, browser и OTA имеют отдельные qualification slices и не задерживают уже полезную диагностику.

При работе нескольких агентов за каждым issue закрепляется один writer. Контрактная ревизия и candidate SHA указаны явно; общие файлы не редактируются одновременно без координатора. Review выполняется read-only по точному кандидату.

## 4. Этапы поставки

| Этап | Что можно принять | Что ещё не утверждается |
|---|---|---|
| A — документы | PRD/architecture/proposed ADR/backlog опубликованы для review | Нет реализованного сервиса или hardware допуска |
| B — offline MVP | Core, ADV adapter и CLI/MCP прошли fake conformance | Не проверены OS/USB и установленная плата |
| C — минимальная плата | Разрешённые connect/status/report подтверждены на точном профиле | Не разрешены автоматически SD/audio/flash |
| D — агентные клиенты | Skills и выбранный вебчат дают тот же результат | Не обещается поддержка любого клиента/аккаунта |
| E — deployment | Plan/apply и постпроверки квалифицированы отдельно | Нет автоматического fleet rollout |
| F — расширения | Browser/config/OTA по собственным profiles | Отсутствие optional функции не регрессия core |

Не закрывать epic после этапа A. D00 может закрыться после review/merge его PR; остальные задачи сохраняют самостоятельные критерии. Недоступный hardware этап отражается BLOCKED, а не PASS.

## 5. Связь с ранее заведённой работой

[#33](https://github.com/ozand/adv/issues/33) остаётся исторической постановкой вариантов доступа. [#35](https://github.com/ozand/adv/issues/35) и [#36](https://github.com/ozand/adv/issues/36) — входные исследования и инвентаризация, не доказательство device capability. [#37](https://github.com/ozand/adv/issues/37) — draft контракта; D02 доводит нужную часть до формальных схем. [#38](https://github.com/ozand/adv/issues/38) используется D01 для сценарных компромиссов в согласованном направлении.

[#2](https://github.com/ozand/adv/issues/2), [#43](https://github.com/ozand/adv/issues/43) и [#64](https://github.com/ozand/adv/issues/64) сохраняют свои аппаратные/source границы и evidence. Новый epic не переоткрывает автоматически их scope и не закрывает их заочно. Принятые ADR не переписываются задним числом.

## 6. Незакрытые решения

Exact dependency pins and transitive license/security qualification, Windows packaging/runtime qualification, implementation numeric bounds, trust/grant implementation, remote client, firmware profiles for config/OTA. Repository/path and stack direction were accepted in D01; details owned by D02, D03, D09, D12/D13 respectively. No install commands are implied by these decisions.
