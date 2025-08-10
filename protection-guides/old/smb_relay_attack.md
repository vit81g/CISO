# SMB Relay (Updated) — Relay Attack for Escalation in Hybrid AD

**Предупреждение:** Используйте только в авторизованных тестах.

## 🎯 Цель атаки
Релей SMB для эскалации привилегий; актуально для unpatched систем в hybrid средах.

## 📋 Условия
- Нет SMB signing.
- Hybrid AD с exposed SMB shares.

## 🔹 Почему Это Работает
Перехват NTLM challenge; relay к другому серверу для доступа от имени жертвы. Усилено в 2025 с EPA, но уязвимо без.

## 🔹 Пошагово
1. Запустить ntlmrelayx.py -t smb://target.
2. Coerce аутентификацию (e.g., PrinterBug).
3. Relay к DC; dump SAM или DCSync.

**Потенциальная ошибка:** Signing required — "Relay failed".

## 📊 SIEM
- Event ID 4624 (Logon Type 3) с unexpected IP.
- **Sigma Rule:** detection: EventID: 4624 AND LogonType: 3

## 🛡 Защита
- Enforce SMB signing.
- Disable NTLMv1; use Kerberos.

## 📌 Вариации
- Комбо с LLMNR для initial access.
