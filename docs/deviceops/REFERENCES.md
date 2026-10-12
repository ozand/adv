# DeviceOps — источники и границы подтверждений

**Дата подготовки:** 2026-10-12. **Epic:** [#66](https://github.com/ozand/adv/issues/66). Этот файл объясняет evidence basis проекта. Ссылка на документацию не означает установленную зависимость, выполненный тест или доступность функции в аккаунте пользователя.

## 1. Источники внутри проекта

Исходный снимок: [ознакомительная ревизия `313e1ddb`](https://github.com/ozand/adv/tree/313e1ddb909c2487d0832b8783d03d06adc44199). Относительные ссылки ниже удобны для навигации; при дальнейшем изменении main сравнивать их с этой ревизией.

| Источник | Что подтверждает / чего не подтверждает |
|---|---|
| [AGENTS.md](../../AGENTS.md), [GOALS.md](../../GOALS.md), [README](../../README.md) | Публичная KB, issue/ADR/PR workflow, ограничения публикации; не разрешение на runtime операции |
| [ADR-006](../adr/ADR-006-hardware-diagnostic-serial-json.md) | Принятый source-контракт четырёх bounded serial-команд; не аппаратный PASS |
| [ADR-009](../adr/ADR-009-bounded-opt-in-audio-diagnostics.md) | Отдельные opt-in audio-команды и cleanup/evidence ограничения |
| [ADR-007](../adr/ADR-007-publish-reviewed-research-captures-exclude-local-source-originals.md) | Границы публичных материалов и исключение source originals/секретов |
| [ADR-013](../adr/ADR-013-define-bounded-batch-knowledge-workflow.md) | Принцип exact-candidate review и разделения gates; не DeviceOps runtime/security implementation |
| [Дорожная карта доступа](../diagnostics/agent-device-access-roadmap.md) | Исторические варианты host/device-side и вопросы исследования |
| [Проект operation contract](../diagnostics/agent-device-operation-contract-draft.md) | Предыдущие proposed semantics и сохранение uncertainty; не принятый public API |
| [Host CLI](../../scripts/adv_diagnostic_cli.py), [скетч](../../scripts/hardware_check/hardware_check.ino) | Реальные исходные точки интеграции; наличие файла не доказывает установленную версию |

Подтверждение владельцем service-centered направления и поручение создать пакет переданы из координационного чата в [epic #66](https://github.com/ozand/adv/issues/66). Это provenance направления, не утверждение о независимом review или принятии всех деталей ADR-014.

## 2. Первичные внешние источники

Официальные страницы ниже рассмотрены как источники возможностей/ограничений при подготовке программы. Подвижные `/stable`, `/latest` и страницы поставщиков не являются lockfile. D01/D06/D09 повторно проверяют нужные версии перед выбором зависимости или подключением аккаунта.

| Источник | Полезный факт | Граница для DeviceOps |
|---|---|---|
| [ESP Web Tools](https://esphome.github.io/esp-web-tools/) | Браузерная установка, serial-интерфейс, firmware manifest и optional Improv | Не общий DeviceOps API, grant engine или гарантия совместимости платы/сохранения данных |
| [ESP-IDF: idf.py MCP server](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/tools/idf-py.html) | В руководстве предусмотрен локальный `idf.py mcp-server` с проектными операциями и ресурсами; требуется соответствующая feature | Кандидат для интеграции tooling; не причина менять SDK прошивки и не обход policy |
| [MCP transports](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports) | Спецификация описывает stdio и Streamable HTTP | Выбранный клиент/SDK должен реально поддерживать согласованную revision; lifecycle DeviceOps не заменяется lifecycle RPC |
| [Web Serial requestPort](https://developer.mozilla.org/en-US/docs/Web/API/Serial/requestPort) | Разрешение порта требует пользовательского действия и соответствующего browser/security context | MCP/Skill не получает таким образом автоматический доступ к USB пользователя |
| [OpenAI Secure MCP Tunnels](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) | Описан исходящий защищённый путь к частному MCP через tunnel client | Доступность в организации/workspace и разрешения проверяются отдельно; не обязательная зависимость core |
| [ESP-IDF OTA](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/ota.html) | OTA slots, проверка/подтверждение новой версии и rollback при соответствующей реализации/конфигурации | Не доказывает наличие OTA или совместимых миграций в текущей ADV firmware |
| [pytest-embedded concepts](https://docs.espressif.com/projects/pytest-embedded/en/latest/concepts/key-concepts.html) | DUT-модель и инструменты embedded-тестирования | Возможные flash/setup эффекты профиля требуют inspection; запуск теста не считается автоматически read-only |

Дополнительная первичная точка проверки упаковки/записи: [esptool basic commands](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/esptool/basic-commands.html). При реализации D07 проверять `merge-bin`, erase/write ranges и параметры конкретной версии, а не копировать адреса из произвольного примера. В этой поставке esptool не запускался.

## 3. Кандидаты, которые не выбраны зависимостями

`esptool-js`, `pytest-embedded`, официальный ESP-IDF MCP и сторонний `DatanoiseTV/esparagus` могут сократить отдельные части реализации. Для esparagus и любых новых кандидатов D01 должен проверить точную ревизию, лицензии, формат результатов и собственную таблицу hardware qualification; прежнее упоминание проекта не заменяет такой проверки.

Device-side MCP и WebMCP — возможные расширения. В MVP не требуется их наличие, обязательная сеть на ESP32 или iframe с USB-полномочиями. Не публиковать версию/совместимость этих механизмов как проверенный факт без актуального первичного источника и теста нужного клиента.

## 4. Правила evidence

Хранить ссылку на утверждение, конкретную версию/SHA, способ проверки и ограничения. Не смешивать source-documented, source-tested, fake-tested и device-observed. Реальные зависимости после выбора записываются в manifest/lockfile своего runtime-репозитория и compatibility report; данный список не является таким manifest.

Новые документы — оригинальное проектное предложение. Здесь не публикуются полный приватный чат, source archives, реальные конфигурации, пароли и аппаратные captures. Факт открытия источника не объявляется результатом его сборки или независимого security audit.
