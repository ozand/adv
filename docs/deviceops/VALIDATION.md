# DeviceOps — проверка и квалификация

**Статус:** план тестов; перечисление не означает выполнение. **Epic:** [#66](https://github.com/ozand/adv/issues/66). **Владелец интеграции:** [D14 / #81](https://github.com/ozand/adv/issues/81).

В этой документационной поставке не реализованы и не выполнены тесты самого DeviceOps. Реальные результаты проверки документов фиксируются в PR/issue receipt, отдельно от будущих fake/client/hardware тестов.

## 1. Уровни доказательств

Source review, source-contract test, fake transport, настоящий клиент с fake device, устройство и независимое физическое измерение — разные уровни. Успех одного не повышает автоматически остальные. У отчёта обязательны точные SHA/версии, scope и NOT_RUN/BLOCKED для отсутствующего этапа.

Для fake suites real serial/network/device backend выключены конструктивно; тест должен падать при попытке их вызова. Работа с временными файлами и synthetic bytes не является разрешением читать реальные secrets/flash/logs.

## 2. Матрица проверок

| ID | Сценарий и ожидаемое свойство | Требование / задача |
|---|---|---|
| V01 | Одинаковый запрос через CLI/MCP: одинаковые normalized results, deny и uncertainty | R01; D06 |
| V02 | Две платы одного chip family: неверный target/grant не вызывает I/O | R02/R04; D03/D05 |
| V03 | Reset/re-enumeration или неизвестный firmware: binding не угадывается, cache не восстанавливается фиктивно | R02; D05/D08 |
| V04 | Неизвестные поля, переполнение каждого лимита, malformed/overlong input отвергаются bounded | R03/R11; D02 |
| V05 | Wrong principal/hash/target, expired grant и самоподтверждение дают deny до dispatch | R04; D03 |
| V06 | Grant отозван после постановки в очередь: запуска не происходит | R04; D03/D04 |
| V07 | Два клиента/worker, expired lease при живом I/O: второй writer не допускается | R05; D04 |
| V08 | Crash до dispatch и на каждой последующей стадии: сохранено правдивое состояние | R06; D04 |
| V09 | Partial write/lost ACK: нет автоматической второй отправки; эффект inconclusive | R06; D04/D05 |
| V10 | Один request_id с тем же payload возвращает job, другой payload даёт конфликт; cancel не равен rollback | R06; D02/D04 |
| V11 | Connect/tools-list/status не запускают run/SD/audio/reset вне явного connection profile | R07; D05/D06 |
| V12 | ADR-006 ID/cache/SD gate и ADR-009 isolation сохраняются; physical PASS не выдуман | R07/R09; D05 |
| V13 | Wrong board/layout/hash/size/trust и пересекающиеся диапазоны блокируют план | R08/R13; D07 |
| V14 | Merged-image gaps/erase sectors учтены; отключение full erase не обещает preservation | R08; D07 |
| V15 | Artifact/plan/target заменён после согласования: apply отвергается; argv allowlist | R08; D07/D08 |
| V16 | Flash завершён, boot/health не подтверждён: deployment не получает неподтверждённый успех | R09; D08 |
| V17 | Синтетические secrets отсутствуют во всех outputs/logs/errors/receipts | R10; D03/D09/D12 |
| V18 | Враждебный лог/SSID/manifest не изменяет полномочия агента или interpreter | R10; D03/D10/D11 |
| V19 | Disk-full, queue overflow, slow reader и restart migration не теряют uncertainty | R11; D04 |
| V20 | Cross-user remote/browser request, stream loss, закрытая вкладка и stale session не обходят policy | R12; D09/D11 |
| V21 | Receipt связан с точным device/profile/artifact/test; неизвестные поля evidence не повышают confidence | R09/R13; D14 |
| V22 | Непроверенный build job не имеет USB/production secrets; stable требует отдельного допуска | R13; D07/D14 |
| V23 | Config conflict/partial apply/network loss: нет затирки и ложного rollback | R14; D12 |
| V24 | Fake OTA boot loop/power loss/failed confirmation/data migration: корректные slot/rollback outcomes | R14; D13 |

Каждая исходная задача добавляет focused tests; D14 соединяет их, а не откладывает все проверки до конца проекта. Точные test names/команды появляются вместе с реализацией и записываются в соответствующий issue.

## 3. Порядок gates

**G0 — проект и место реализации.** Принятые детальные решения, версии, path allowlist и traceability. Подготовка draft/fake fixtures не требует устройства.

**G1 — offline conformance.** Обязательные случаи локального MVP проходят с fake backend; все реальные I/O запрещены. Security отрицательные тесты и crash/replay проверки обязательны.

**G2 — клиентская интеграция.** CLI/MCP и выбранный remote client проверяются на fake device. Подключение аккаунта/туннеля разрешается отдельно. Не требуется ждать optional браузера/config/OTA.

**G3 — минимальная аппаратная сессия.** Отдельное согласие на точный target/connection profile/команды. Проверяются connect/status/report, без implicit run/SD/audio/flash. При другой установленной прошивке остановка, а не самовольная переустановка.

**G4 — изменяющие состояние сценарии.** Bounded run, SD, audio, deployment, config, OTA и power-cut каждый требуют своих эффекта/допуска/recovery. Offline D08/D13 не зависит от G4; G4 проверяет уже прошедший fake-review код, поэтому цикла зависимостей нет.

## 4. Аппаратный checklist

Перед сессией оператор подтверждает идентичность платы, текущую прошивку и ценность сохраняемых данных, кабель/питание, владельца порта, допустимые действия, stop conditions и доступный recovery. Эти сведения могут быть приватными; публично фиксируется sanitized receipt.

Первое действие не должно сбрасывать или прошивать устройство под видом обнаружения. Если serial open меняет линии и может reset, это заранее видно в профиле и согласии. При занятом порте не завершать чужие процессы автоматически.

Во время выполнения: сохранить operation/session identity, ограниченный результат и факт всех отправок; при неожиданной перепрошивке/сбросе/эффекте остановить новые действия. Не запускать SD/audio автоматически ради «полноты» отчёта. Проверки экрана/клавиатуры/акустики требуют реального наблюдения, а не только self-report firmware.

После сессии: подтвердить закрытие I/O, состояние устройства, revoke временные права и применить retention. Неполученный результат остаётся INCONCLUSIVE, даже если оператор предполагает успех.

## 5. Формат передачи результатов

Минимальный receipt: governing issue; candidate SHA; versions core/adapter/firmware/toolchain; разрешённый профиль/plan reference; обезличенная target identity и её сила; время; test IDs; expected/actual; стадии передачи/ACK/verification; эффекты; результат cleanup/recovery; ограничения; местонахождение приватного evidence по разрешённой reference.

Не публиковать runtime DB, токены, полный MAC/USB serial, сырые логи или дампы. Independent reviewer указывается только при фактически выполненном review точного кандидата. Собственная повторная проверка агента не называется независимой.

## 6. Приёмка этапов

MVP-A принимается отдельно от hardware. Если G3 недоступен, offline результат может быть завершён, а hardware остаётся BLOCKED. Это не закрывает D14 целиком без выполнения его scope или явного изменения владельцем.

Optional браузер, настройка и OTA имеют собственные qualification profiles. Появление ещё одного транспорта не требует повторять весь проект, но требует доказать сохранение policy/identity/uncertainty invariants и проверить его специфические сбои.
