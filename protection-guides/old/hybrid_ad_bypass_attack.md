# Hybrid AD Authentication Bypass — Entra ID Sync Abuse

**Предупреждение:** Используйте только в авторизованных тестах.

## 🎯 Цель атаки
Байпас аутентификации для кражи данных (emails, docs) в hybrid AD/Entra ID.

## 📋 Условия
- Entra Connect для sync AD с Entra ID.
- Компромисс sync-сервера (lateral movement).
- Hybrid Exchange с SSO.

## 🔹 Почему Это Работает
Извлечение cert/private key из Entra Connect; генерирует unsigned S2S-токены (24h valid), байпас MFA.

## 🔹 Пошагово
1. Компромисс Entra Connect (credential dump).
2. Извлечь cert/key.
3. Генерировать токены; impersonate users (soft matching).
4. Запрос S2S-токенов для mailbox access.
5. Exfiltrate data; манипулировать Graph API (add backdoor keys).

**Потенциальная ошибка:** No logs — blind spot; unusual Graph calls.

## 📊 SIEM
- Unauthorized cert exports.
- Graph API calls с Directory.ReadWrite.All.
- **ELK Query:** "api: Graph AND permission: Directory.ReadWrite.All"

## 🛡 Защита
- Hardware key storage.
- Rotate SSO keys.
- Zero-trust; segregate hybrid services (MS mandate Oct 2025).

## 📌 Вариации
- Mailbox impersonation; policy manipulation for persistence.
