# SMB/LDAP Hardening

## 🎯 Цель
Предотвратить атаки на SMB и LDAP протоколы (Relay, MITM, перехват хэшей).

## 🔹 Меры защиты
- Включить SMB signing (Require) на серверах и критичных хостах.
- Включить LDAP signing + Channel Binding.
- Отключить анонимный доступ к SMB и LDAP.
- Применить UNC Hardening (RequireMutualAuth, RequireIntegrity).
- Ограничить доступ к административным шарам (`C$`, `ADMIN$`).

## 📊 Мониторинг
- Event ID 5140, 5145 — доступ к общим ресурсам.
- Event ID 2886, 2887, 2889 — LDAP Bind без подписи.
