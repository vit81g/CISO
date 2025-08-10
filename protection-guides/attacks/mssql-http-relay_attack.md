# MSSQL Relay / HTTP Relay (ntlmrelayx)

## 🎯 Цель атаки
Использовать перехваченную NTLM‑аутентификацию для выполнения действий на **MSSQL** или **HTTP** сервисах.

## 📋 Описание
ntlmrelayx поддерживает целевые протоколы SMB/LDAP/HTTP/MSSQL.  
При уязвимой конфигурации (нет Channel Binding / Extended Protection / подписи) возможно выполнение команд на MSSQL (`xp_cmdshell`) или злоупотребление контекстом на HTTP.

## ⚠ Условия эксплуатации
- На цели отключены/не настроены защитные механизмы (Signing/EP/CB).
- Перехват NTLM возможен (LLMNR/WPAD/MITM6/PrinterBug и т.п.).

## 🔹 Пошагово в лаборатории
> ⚠ Только в изолированной среде!

### MSSQL Relay
1. Запускаем релей на MSSQL с выполнением команды:
```bash
ntlmrelayx.py -t mssql://10.0.0.55 --execute "xp_cmdshell 'whoami'"
```
2. При аутентификации жертвы команда выполнится в контексте её прав на MSSQL.

### HTTP Relay
1. Релей на HTTP‑приложение (пример — перечисление локальных админов/ресурсов):
```bash
ntlmrelayx.py -t http://intranet.lab.local --enum-local-admins
```
2. Используем дополнительные действия (`--dump-laps`, `--adcs` и т.д.) когда поддерживается.

## 📊 Признаки в логах и мониторинг
- MSSQL: события выполнения `xp_cmdshell`, лог‑инстанс агента.
- HTTP: логи аутентификации NTLM с неожиданных клиентов.
- 4624 Type 3 на целях релея.

## 🛡 Меры защиты
- Включить **Extended Protection**/**Channel Binding** на HTTP/IIS.
- Отключить `xp_cmdshell` на MSSQL и применять подпись NTLM где возможно.
- Запрет NTLM/принудительный Kerberos.

## 🔗 Источники
- ntlmrelayx documentation / MSSQL & HTTP relay research

---

## 🔍 Разбор команд

### 1. Релей на MSSQL и выполнение команды
```bash
ntlmrelayx.py -t mssql://10.0.0.55 --execute "xp_cmdshell 'whoami'"
```
- **`-t mssql://...`** — цель MSSQL.
- **`--execute "xp_cmdshell '...'"`** — выполнить системную команду через расширенную хранимую процедуру.

### 2. Релей на HTTP
```bash
ntlmrelayx.py -t http://intranet.lab.local --enum-local-admins
```
- **`-t http://...`** — цель HTTP.
- **`--enum-local-admins`** — одна из встроенных операций для целевого хоста/приложения.
