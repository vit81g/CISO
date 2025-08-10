# Hardening Active Directory (Updated for 2025)

## 🎯 Цели
Усиление безопасности инфраструктуры Active Directory с учётом новых техник атак 2025 года: **BadSuccessor**, **Golden dMSA**, **Kerberoasting (gMSA)**, **AD Trusts Attack Paths**.

## ⚠ Угрозы
- Эскалация привилегий через подмену и брутфорс dMSA (BadSuccessor, Golden dMSA).
- Кража сервисных учёток через Kerberoasting.
- Междоменный компромисс через trust-отношения (AD Trusts Attack Paths).

## 🛡 Меры защиты
### 1. Управляемые сервисные аккаунты (gMSA/dMSA)
- Ограничить права на чтение атрибутов `msDS-ManagedPassword` и `ManagedPasswordId`.  
  **MITRE ATT&CK:** T1003.006 (LSASS Memory), T1552.004 (Private Keys)
- Использовать длинные случайные пароли для gMSA (автогенерация каждые 30 дней).
- Мониторить события **4662** (доступ к объектам AD) для dMSA.

### 2. Kerberos
- Установить флаг **PreAuthentication required** для всех учёток.  
  **MITRE ATT&CK:** T1558.003 (Kerberoasting)
- Мониторить события **4769** (выдача TGS).
- Ограничить выдачу TGS по SPN.

### 3. AD Trusts
- Запретить использование SIDHistory между доменами.  
  **MITRE ATT&CK:** T1134.005 (SID-History Injection)
- Включить аудит событий **4765**/**4766** (изменение SIDHistory).
- Ограничить Kerberos делегацию между доменами.

### 4. Администрирование
- Использовать отдельные административные леса или PAM.
- Применять Tiered Admin Model (разделение админских учёток).

## ⚙ Настройка
### Пример GPO для отключения SIDHistory
```powershell
Set-ADForest -Identity corp.local -SIDHistoryQuarantine $true
```
### Пример поиска уязвимых dMSA
```powershell
Get-ADServiceAccount -Filter * -Properties msDS-ManagedPasswordId
```

## 📌 Дополнительно
- **MITRE ATT&CK:** T1003.006, T1552.004, T1558.003, T1134.005  
- [Microsoft Securing Privileged Access](https://learn.microsoft.com/en-us/microsoft-365/compliance/securing-privileged-access)  
- [SpecterOps AD Security](https://specterops.io/)  
