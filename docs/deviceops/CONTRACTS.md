# DeviceOps — проект контрактов

**Статус:** proposed semantics, не опубликованный стабильный API. **Задача:** [D02 / #69](https://github.com/ozand/adv/issues/69). **Epic:** [#66](https://github.com/ozand/adv/issues/66). Формальные схемы, numeric bounds и версии принимает отдельный review; wire-контракты ADV этим документом не меняются.

## 1. Сущности

| Сущность | Содержание |
|---|---|
| Device | Логический `device_id`, профиль, ожидаемая плата, известная firmware и источники этих сведений |
| Binding/session | Конкретный executor, transport locator, поколение сессии, identity evidence и время наблюдения |
| Capability | Именованная операция, версия, совместимые firmware, schemas, effects, limits, authority, retry/cancel/recovery rules |
| Request | Client `request_id`, нормализованные аргументы и target; principal передаётся доверенным frontend context |
| Operation | Долговечный host `operation_id`, request digest, plan/grant ссылки, lifecycle и события |
| Plan | Неизменяемый target-bound набор действий, проверок и эффектов с digest |
| Grant | Выданное доверенной стороной ограниченное разрешение; модель его не создаёт |
| Evidence/receipt | Результат, provenance, границы наблюдения и verification status |

`device_id` — административное имя, а не аппаратная аттестация. `session_generation` — host bookkeeping, не firmware `boot_id`. Не добавлять фиктивный boot counter в ответы старой прошивки. Для опасных операций минимальная сила identity задаётся policy.

## 2. Каталог операций

Имена — проект будущего DeviceOps API, не команды ESP Web Tools и не новая firmware ABI.

| Операция | Смысл / эффект |
|---|---|
| `device_list` | Разрешённый реестр известных устройств; без автоматического открытия портов |
| `device_inspect` | По умолчанию cached metadata с возрастом; fresh probe — отдельная явно разрешённая операция |
| `device_capabilities` | Пересечение профиля, известной firmware, состояния и policy; неизвестное не становится доступным |
| `device_connect` | Явное открытие транспорта по connection profile; возможные управляющие линии/reset отражены в effects |
| `diagnostic_start` | Только именованный разрешённый test profile; в MVP статус либо отдельно разрешённый bounded run |
| `operation_get` / `report_get` | Чтение сохранённого host-состояния; не повторная отправка команды устройству |
| `diagnostic_result_query` | Отдельное чтение retained firmware result, когда session/cache semantics позволяют |
| `deploy_plan` / `deploy_execute` | Планирование без hardware I/O и отдельное исполнение согласованного плана |
| `config_plan` / `config_apply` | Только для принятого firmware/config profile |
| `logs_read` | Ограниченные redacted данные, если такой источник отдельно поддержан; не raw console по умолчанию |

В списке MCP доступны только реально реализованные capabilities. Необходимость новой операции оформляется отдельным контрактом, а не аргументом `arbitrary_command`.

## 3. Декларация эффектов

Одного `read_only` недостаточно. Для capability описываются: cached/fresh I/O, открытие транспорта и reset, volatile state, persistent storage, физический audio/RF output, внешние сетевые эффекты и раскрываемые данные. Также обязательны prerequisites, минимальное разрешение, предел времени ожидания, границы сообщения/результата, допустимый concurrency, сохранность результата и восстановление.

D02 фиксирует конечные пределы request/response, log page, queue depth, retained jobs/events, TTL планов/разрешений и wait timeout. Это конфигурация host с тестами на границах; она не увеличивает firmware frame bounds. Для каждого adapter deadline отдельно указать: это предел ожидания хоста или доказанный предел исполнения устройства. Превышение первого не доказывает остановку второго.

## 4. Lifecycle и результат

Предлагаемый основной путь: `accepted -> queued -> running -> terminal`. Терминальные состояния: `succeeded`, `failed`, `inconclusive`, `cancelled`. Запрос, отклонённый schema/policy до принятия задания, возвращает rejection без dispatch. Стадия выполнения хранится отдельно, например `preflight`, `writing`, `awaiting_device`, `verifying`.

| Состояние | Допустимый смысл |
|---|---|
| `succeeded` | Выполнена postcondition этой операции; успешное чтение статуса не означает исправность всей платы |
| `failed` | Установленная ошибка; effects могут быть `none`, `known_partial` или `known_completed` и описываются отдельно |
| `inconclusive` | Результат/эффект неизвестен; timeout, partial write или потеря ACK не превращаются в повтор |
| `cancelled` | Отмена до dispatch либо подтверждённая безопасная остановка; предыдущие эффекты явно сохранены |

Дополнительные поля: `transmission` (`not_attempted`, `partial`, `complete`, `unknown`), `device_ack` (`not_received`, `received`, `unknown`), `effect_certainty` (`none`, `known_partial`, `known_completed`, `unknown`), `verification` (`not_attempted`, `passed`, `failed`, `inconclusive`). Проверки физического оборудования имеют собственные `PASS`, `FAIL`, `NOT_TESTED`, `INCONCLUSIVE` из профиля; их нельзя вычислять из host state.

Упрощённый синтетический пример, не фактическая операция и не окончательная JSON Schema:

```json
{
  "schema_version": "0.1-draft",
  "operation_id": "example-op-001",
  "device_id": "example-adv",
  "session_generation": 7,
  "state": "inconclusive",
  "stage": "awaiting_device",
  "reason": "ack_timeout",
  "transmission": "complete",
  "device_ack": "not_received",
  "effect_certainty": "unknown",
  "verification": "not_attempted",
  "automatic_retry_allowed": false,
  "evidence_kind": "synthetic"
}
```

Завершённые записи не переписываются незаметно. Позднее подтверждение или reconciliation добавляет связанное evidence/задание и историю переходов. `operation_get` само не возобновляет исполнение.

## 5. Повторы, crash и отмена

Ключ дедупликации включает principal, target и client `request_id`. Тот же ключ с тем же normalized request digest возвращает существующий operation; другой digest — конфликт. Срок хранения дедупликации объявляется клиенту; после истечения нельзя обещать защиту от повторного внешнего действия.

Журналирование на хосте не делает serial-команду exactly-once. Передача могла произойти до сбоя DB/процесса. После неопределённой передачи mutating операция не отправляется автоматически: сначала допустимая проверка retained результата либо остановка до решения оператора. Restore DB и смена executor не обходят это правило.

Отмена ожидания клиентом отличается от cancellation request задания. Уже начатая запись останавливается только в разрешённой безопасной точке либо доводится исполнителем до оговорённого состояния. Отмена не равна rollback. Lease удерживается до подтверждённого завершения I/O или session quarantine.

## 6. Совместимость с текущим ADV

Источники: [ADR-006](../adr/ADR-006-hardware-diagnostic-serial-json.md), [ADR-009](../adr/ADR-009-bounded-opt-in-audio-diagnostics.md), [host CLI](../../scripts/adv_diagnostic_cli.py), [скетч](../../scripts/hardware_check/hardware_check.ino). Это исходники и принятые source-контракты, не доказательство установленной firmware или аппаратного PASS.

ADR-006 задаёт строки `status`, `sd_test`, `run <ID>`, `result <ID>`, предел командной строки 64 байта, ID из 1–12 uppercase ASCII letters/digits, v1 status/SD и v2 run/result frames до 1024 байт. `status` читает cached сведения без SD. SD — отдельный one-shot opt-in; `run` не включает SD автоматически. Один результат хранится в RAM: тот же ID возвращает кэш, другой при занятом слоте отклоняется, reset теряет запись.

Host `operation_id` не отправляется напрямую как firmware ID. D05 ведёт явное соответствие с допустимым коротким ID и текущей сессией; после reset не заявляет прежний результат сохранённым. Старый ID после reset не делает повтор безопасным.

ADR-009 добавляет отдельные mic/tone операции и result queries без изменения старых wire shapes. Общий marker новой исходной прошивки — `adv-diagnostic-3-audio-proposal`; совместимость старых потоков с `adv-diagnostic-2` проверяется существующим host-валидатором. Marker — только информационное evidence. Audio-profile не входит в MVP, не вызывается при connect/run и не отправляет raw samples. Его будущая интеграция должна сохранить cleanup uncertainty и отсутствие acoustic PASS без независимого наблюдения.

## 7. Ошибки и evidence

Предлагаемые reason families: invalid_request, permission_denied, unsupported_capability, identity_ambiguous, device_busy, session_changed, incompatible_firmware, limit_exceeded, transport_error, ack_timeout, result_unavailable, plan_changed, artifact_untrusted, verification_failed. Окончательные enum и mapping firmware reasons фиксирует D02; неизвестный upstream текст не передаётся как исполняемая инструкция или свободная ошибка.

Receipt содержит точные доступные версии core/adapter/firmware, request/plan/artifact references, observation time, session/identity confidence, стадии и тестовый профиль. Реальные идентификаторы минимизируются. Уровни evidence (`source_documented`, `source_tested`, `fake_tested`, `client_tested`, `device_observed`, `externally_verified`) относятся к конкретному утверждению, а не автоматически ко всему устройству.

Формальный контракт считается готовым после negative fixtures и review D02/D03. Примеры здесь служат входом для этой работы и не должны подключаться к production parser как неявный стандарт.
