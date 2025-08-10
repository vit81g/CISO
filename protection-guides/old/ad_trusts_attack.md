# AD Trusts Attack Paths — Inter/Intra-Forest Compromise via BloodHound

**Предупреждение:** Используйте только в авторизованных тестах.

## 🎯 Цель атаки
Компромисс домена через trust-отношения (intra/inter-forest).

## 📋 Условия
- Trust между доменами (same-forest bidirectional; cross-forest с weak config: TGT delegation, no SID filtering).

## 🔹 Почему Это Работает
Trusts позволяют транзитивный доступ; weak настройки (e.g., no quarantine) разрешают spoof SID, TGT capture.

## 🔹 Пошагово
1. Собрать данные (BloodHound: sharphound.exe --CollectionMethods All).
2. Идентифицировать paths (SameForestTrust, AbuseTGTDelegation, SpoofSIDHistory).
3. Для SpoofSIDHistory: Mimikatz sid::patch; добавить SID (e.g., Enterprise Admins).
4. Для AbuseTGTDelegation: Coerce DC to unconstrained delegation; capture TGT; DCSync.
5. Для Trust Account: Mimikatz lsadump::trust /patch; аутентифицироваться как trust account.

**Потенциальная ошибка:** SID filtering enabled — "Access Denied".

## 📊 SIEM
- Event ID 4662: DCSync после TGT.
- Event ID 5136: Изменения Configuration NC.
- Event ID 4768: TGT requests across trusts.
- **Sigma Rule:** detection: EventID: 4768 AND TargetDomain: *external*

## 🛡 Защита
- Включить SID filtering (quarantine).
- Отключить TGT delegation.
- Мониторить trustAttributes (Get-ADTrust).

## 📌 Вариации
- Coerce to TGT; ADCS ESC5 в forest.
