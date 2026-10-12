# DeviceOps — артефакты, развёртывание и настройка

**Статус:** проект workflow, не готовая инструкция прошивки конкретной платы. **Epic:** [#66](https://github.com/ozand/adv/issues/66). Задачи: [D07](https://github.com/ozand/adv/issues/74), [D08](https://github.com/ozand/adv/issues/75), [D12](https://github.com/ozand/adv/issues/79), [D13](https://github.com/ozand/adv/issues/80).

## 1. Единый каталог, разные представления

Каталог хранит versioned artifact descriptor. Из него строятся DeviceOps plan, задания проверки и необязательный ESP Web Tools manifest. Обратное преобразование произвольного EWT manifest в безопасный plan не предполагается: в нём недостаточно сведений о нашей policy и совместимости.

| Поле descriptor | Для чего нужно |
|---|---|
| Artifact identity/kind/digest/size | Точные bytes; factory, application OTA и resource package различаются |
| Board/revision/chip/flash requirements | Совместимость конкретного устройства, не только ESP32 family |
| Build provenance | Repo/commit, toolchain и профиль сборки, adapter/tool versions |
| Parts: offset/length/hash | Разрешённые диапазоны записи и фактические erase ranges |
| Layout/settings schema compatibility | Допустимые переходы, миграции и несовместимые исходные состояния |
| Trust metadata | Одобренный издатель/источник, подпись или явно ограниченный lab trust |
| Post-boot/health/recovery profile | Что и как проверяется после установки; доступность отката |
| Qualification evidence | Отдельно compile/fake/hardware результаты с точной конфигурацией |

D07 принимает формальную схему и synthetic fixtures. В `adv` не размещаются готовые binaries или приватные captures; место каталога/релизов определяется D01.

## 2. Подготовка plan без скрытого I/O

`deploy_plan` принимает разрешённый artifact reference и snapshot известных сведений об устройстве. Недостающие факты не добываются неявным reset или чтением flash: возвращаются blocker и требуемая отдельная операция проверки.

План фиксирует target binding, artifact/parts, текущую известную layout, версию policy/adapter, ожидаемые эффекты, erase/write ranges, data-loss/backup требования, checks и recovery. Digest строится по определённому каноническому представлению; bytes сохраняются immutable либо повторно проверяются при apply. D02/D07 должны исключить неоднозначности нормализации.

Проверяются размеры, переполнения адресов, пересечения, границы flash и erase-sector alignment. Нельзя брать offsets из универсального примера. У объединённого RAW-образа промежутки тоже могут попасть в записываемый/стираемый диапазон; поэтому «erase whole chip выключен» не является гарантией сохранения данных. Источники упаковки образов: [REFERENCES](REFERENCES.md).

Привязка plan к точным bytes не доказывает доверие издателю. Hash и signature/trust policy решают разные задачи. Источники, redirect, symlink/path traversal, ограничение размера и подмена между plan/apply входят в проверки.

## 3. Исполнение

```text
resolve immutable artifact
  -> validate plan and target
  -> obtain operator/policy grant
  -> persist operation
  -> reserve device / recheck prerequisites
  -> handoff to bootloader when required
  -> write / verify image
  -> rebind runtime session
  -> check firmware identity and health
  -> receipt or explicit recovery_required
```

`deploy_execute` получает сохранённый plan reference, а не произвольный URL и набор flash offsets. Перед dispatch повторно проверяются bytes, grant, identity и lease. Backend запускается с allowlisted argv, без shell interpolation. Никаких автоматических `--force`, eFuse, полного erase или отключения secure boot ради успешного результата.

После перехода runtime/ROM USB может измениться. Сервис связывает новое подключение с целевым устройством по квалифицированному профилю; если связь неоднозначна, останавливается. Обнаружение того же chip family недостаточно.

## 4. Что означает успех

Отдельно фиксируются: запись завершена, bytes проверены, приложение загрузилось, заявленная версия соответствует ожиданию, health profile выполнен, требуемое внешнее наблюдение получено. Нельзя выводить последний пункт из первых.

Если firmware marker не аутентифицирован, receipt прямо указывает силу этого evidence. Если post-boot API отсутствует, flash task может подтвердить только установку образа; deployment с требованием health остаётся неполным, а не получает фиктивный PASS.

Клиентский timeout не прерывает автоматически критическую запись. После сбоя процесса/USB повторная запись не стартует вслепую. Сначала разрешённое reconciliation; если оно невозможно, фиксируется неизвестный эффект и предложенный recovery plan. План восстановления — отдельное действие, кроме заранее одобренного безопасного сценария с явным scope.

## 5. Сохранение и восстановление данных

Factory install/recovery считается потенциально разрушающим данные внутренней flash. OTA-приложение не является полным factory image. Resource package устанавливается по отдельному профилю, не прошивальщиком ROM.

Резервное копирование — тоже операция с доступом к приватным данным. Оно не запускается по умолчанию как «безопасный» шаг. Нужны разрешённые разделы/поля, место хранения, шифрование/retention и проверенный restore. Полный flash dump может содержать секреты и не публикуется.

Политика сохранения охватывает первый запуск новой прошивки, миграции NVS/файлов и доступ к внешней SD. Отсутствие записи на карту в ROM-прошивальщике не доказывает, что её не изменит установленное приложение.

Recovery может требовать физического действия оператора и известного рабочего образа. ROM download mode/защита чипа ограничивают доступные способы; DeviceOps не обещает универсального восстановления и не снимает аппаратную защиту. Конкретный runbook квалифицируется для target, не копируется между платами автоматически.

## 6. Настройка: config plan/apply

D12 выбирает реальный firmware API и ограниченный набор полей. План показывает redacted diff, текущую revision, требования reboot/network change и postcondition. Apply использует optimistic concurrency; конфликт ревизии требует нового плана, а не перезаписи настроек другого клиента.

Значения секретов разрешает trusted provider. Агент и публичный receipt видят только допустимую reference и результат. При потере сети во время смены Wi-Fi эффект может остаться неизвестным; нельзя повторять применение или объявлять rollback без подтверждения.

Improv — кандидат для Wi-Fi provisioning при поддержке в прошивке, не универсальный config API. Текущий диагностический ADR-006 общего config API не предоставляет. Добавление firmware-функций требует отдельной задачи и решения в репозитории соответствующей прошивки.

## 7. OTA: отдельный профиль, не свойство MCP

D13 требует точной реализации bootloader/partition layout, неактивного слота, image validation, activation, post-boot confirmation и условий rollback. ESP-IDF предоставляет соответствующие механизмы, но их наличие в SDK не доказывает настройку конкретной прошивки; первичная документация приведена в [REFERENCES](REFERENCES.md).

Следует различать `downloaded`, `installed`, `booted`, `confirmed` и `rolled_back`. Доступность сети после reboot сама по себе не подтверждает нужную сборку. Откат приложения не восстанавливает автоматически необратимо мигрированные пользовательские данные. Downgrade/anti-rollback правила входят в профиль.

OTA failure не запускает USB factory erase без нового плана и разрешения. Power-loss тестирование проводится сначала на fake model, затем только по специальному аппаратному допуску.

## 8. Агентная разработка и CI

Build sandbox производит артефакт; policy выбирает допустимость его установки на выделенный стенд; executor выполняет ограниченный тест; агент анализирует receipt. CI из непроверенного PR не получает USB/секреты напрямую. Для автоматического lab-cycle задаются target, набор тестов, бюджет числа прошивок и stop conditions. Публикация stable-релиза требует отдельной квалификации: successful build не равен hardware-tested.
