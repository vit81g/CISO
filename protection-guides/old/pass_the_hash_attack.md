# Pass-the-Hash — Lateral Movement without Passwords

**Предупреждение:** Используйте только в авторизованных тестах.

## 🎯 Цель атаки
Латеральное движение с хэшем NTLM; байпас MFA в hybrid.

## 📋 Условия
- Захваченный NTLM хэш.
- Нет PAM/PTA в hybrid.

## 🔹 Почему Это Работает
Аутентификация с хэшем вместо пароля.

## 🔹 Пошагово
1. Mimikatz sekurlsa::pth /user:admin /domain:local /ntlm:hash.
2. Доступ к shares/RDP/WinRM.

**Потенциальная ошибка:** LSA Protection — blocked.

## 📊 SIEM
- Event ID 4624 с Logon Type 9.

## 🛡 Защита
- LSA Protection; no NTLM.

## 📌 Вариации
- Over-PTH в hybrid для cloud access.
