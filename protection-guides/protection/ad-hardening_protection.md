# Active Directory Hardening

## 🎯 Цель
Укрепление безопасности инфраструктуры Active Directory и уменьшение поверхности атаки.

## 🔹 Меры защиты
- Отключить NTLM (Restrict NTLM) и SMBv1.
- Использовать Kerberos-only для админских учёток.
- Включить AES-only для сервисных аккаунтов.
- Ограничить вход админских учёток (Admin Tiering, PAW).
- Включить Protected Users group для критичных учёток.
- Регулярно проверять и чистить устаревшие объекты AD.
- Включить аудит Directory Services Changes.
