# Чек-лист защиты от атак на NTLM/Relay (DC/DHCP/Hosts)

## 1. Сетевой уровень
- [ ] **Отключить LLMNR и NBNS** на всех рабочих станциях (GPO: `Turn off multicast name resolution`).
- [ ] **Отключить WPAD** и автоопределение прокси (`Automatically detect settings` → Off).
- [ ] **Включить DHCP Snooping** на коммутаторах (только авторизованные DHCP-сервера).
- [ ] **Включить Dynamic ARP Inspection (DAI)** и **IP Source Guard** для защиты от MITM на L2.
- [ ] **Egress ACL**: запретить исходящий трафик 445/389/88 из пользовательских VLAN на внешние сегменты.
- [ ] Сегментировать сеть: изолировать DC, админ-хосты, серверы, критичные системы.

## 2. Протоколы SMB/LDAP/Kerberos
- [ ] **SMB signing** — *Require* на серверах и критичных станциях.
- [ ] **LDAP signing + Channel Binding** — включить (сначала Audit, потом Require).
- [ ] **Restrict NTLM**:
  - Режим Audit (записать, кто куда ходит по NTLM).
  - Этапно запретить NTLM на DC.
- [ ] **UNC Hardening**: `RequireMutualAuth=1, RequireIntegrity=1` для административных шар.
- [ ] **Kerberos-only** для админских учёток (AES-only, Protected Users).

## 3. Политики учётных записей
- [ ] Разделить админские и пользовательские учётки (No DA на рабочей станции).
- [ ] Запретить вход админских учёток на неадминские хосты (GPO: `Deny log on locally` / `Deny log on through RDP`).
- [ ] Включить **Just Enough Administration (JEA)**.
- [ ] Применить MFA для удалённых админ-сессий.

## 4. Мониторинг (SIEM/лог-сбор)
- [ ] **DC**:
  - 4776 — NTLM authentication to DC.
  - 4624/4625 (Logon Type 3) — сетевые логины.
  - 4648 — логин с указанием учётки/пароля вручную.
  - 5140/5145 — доступ к шарам.
  - 4741/4742 — создание/изменение компьютеров в AD.
  - LDAP Bind без подписи (Directory Service log, EventID 2886/2887/2889).
- [ ] **Клиенты**:
  - NTLM-аутентикации на нестандартные IP/имена.
  - Изменение сетевых настроек (DHCP-опции, DNS, шлюз).
- [ ] **Сеть**:
  - DHCP Snooping violations.
  - Аномальные DNS-запросы: `wpad`, короткие однобуквенные имена.

---

# ⚙ Impacket — учебные сценарии

## 1. Аутентификация через хеш (Pass-the-Hash)
```bash
psexec.py DOMAIN/user@target -hashes :<NTLM_HASH>
```
- **Риск**: Злоумышленник входит в систему без знания пароля.
- **В SIEM смотреть**:
  - 4624 (Logon Type 3) с NTLM и `Logon Process: NtLmSsp`.
  - Источник входа ≠ ожидаемого IP пользователя.
- **Защита**:
  - Запрет NTLM (Restrict NTLM).
  - SMB signing Required.
  - Изоляция админских учёток (No local logon).

## 2. Аутентификация админа на скрытой административной шаре `$`
```bash
smbclient.py DOMAIN/user@target -hashes :<NTLM_HASH> -share C$
```
- **Риск**: Доступ к файловой системе хоста.
- **В SIEM смотреть**:
  - 5140 (доступ к `C$`/`ADMIN$`).
  - 4624 (Logon Type 3) от нетипичных источников.
- **Защита**:
  - Запрет админских учёток на рабочих станциях.
  - Ограничение доступа к административным шарам по ACL.

## 3. Добавление в домен нового хоста (LDAP-Relay)
```bash
ntlmrelayx.py -t ldap://dc.domain.local --add-computer 'LAB$' -domain-sid <SID>
```
- **Риск**: Злоумышленник добавляет контролируемый компьютер в домен.
- **В SIEM смотреть**:
  - 4741 (Computer account created).
  - Источник — неавторизованный админ.
- **Защита**:
  - Включить LDAP signing + Channel Binding.
  - Ограничить `MachineAccountQuota=0` (по умолчанию 10).
  - SIEM-алерт на создание компьютеров вне Change-Window.

## 4. Изменение пароля учётной записи (LDAP-Relay)
```bash
ntlmrelayx.py -t ldap://dc.domain.local --escalate-user someuser
```
- **Риск**: Смена пароля жертвы без её ведома.
- **В SIEM смотреть**:
  - 4723 (Change password).
  - Источник ≠ ожидаемого рабочего места пользователя.
- **Защита**:
  - LDAP signing Required.
  - Audit Directory Service Changes.
  - SIEM-правило на смену пароля вне Change-Window.

---

# 📊 Резюме по защите
- Запрет NTLM и SMB/LDAP без подписей.
- Отключение LLMNR/WPAD.
- DHCP Snooping + фильтрация трафика на L2.
- Разделение админских/пользовательских учёток.
- SIEM-алерты по:
  - NTLM логонам с необычных IP.
  - Доступу к `C$`/`ADMIN$`.
  - Созданию/изменению машинных аккаунтов.
  - Смене паролей вне плана.
