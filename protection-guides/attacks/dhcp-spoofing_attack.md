# DHCP Spoofing Attack

## 🎯 Цель атаки
Подменить сетевые параметры хоста (DNS/WPAD/Gateway), направив трафик через атакующего (MITM) и спровоцировав NTLM-аутентификацию на контролируемые сервисы.

## 📋 Описание
Без защиты на L2 (DHCP Snooping/DAI/IP Source Guard) клиент может принять конфигурацию от фальшивого DHCP.  
Указав поддельный **DNS**, **WPAD** или **шлюз**, злоумышленник перенаправляет запросы к себе и релеит NTLM (ntlmrelayx).

## ⚠ Условия эксплуатации
- Отсутствует DHCP Snooping/DAI/IP Source Guard.
- Пользовательский сегмент уровня 2 (тот же VLAN).
- Клиенты используют автонастройку прокси (WPAD) и/или получают DNS по DHCP.

## 🔹 Пошагово в лаборатории
> ⚠ Только в изолированной тестовой среде!

1. **Запуск отравления DHCP** (примерно; утилиты зависят от дистрибутива, в Kali можно использовать yersinia / dhcpig / ettercap-плагины):
```bash
sudo yersinia -I
```
2. **Выдавать клиентам фальшивый DNS/WPAD**, указывая IP атакующего.
3. **Запуск релеера** на LDAP/SMB/HTTP:
```bash
ntlmrelayx.py -t ldap://dc01.lab.local --add-computer
```
4. Когда клиент обратится к ресурсу (через DNS/WPAD) — его NTLM-аутентификация будет релеится на выбранный сервис.

## 📊 Признаки в логах и мониторинг
- Логи коммутаторов: **DHCP Snooping violations**.
- На клиентах: внезапная смена DNS/Proxy/Gateway.
- На серверах: 4624 (Logon Type 3) от нетипичных IP, LDAP unsigned binds (2886/2887/2889).

## 🛡 Меры защиты
- Включить **DHCP Snooping**, **DAI**, **IP Source Guard**.
- Запретить **WPAD** и автоопределение прокси.
- Жёстко задавать DNS через GPO.
- SMB/LDAP signing + Restrict NTLM.

## 🔗 Источники
- Cisco Secure: DHCP Snooping / DAI
- Microsoft: LDAP Signing and Channel Binding

---

## 🔍 Разбор команд

### 1. Yersinia (интерактивный режим)
```bash
sudo yersinia -I
```
- **`-I`** — интерактивный TUI; из меню выбирают протокол **DHCP** и сценарий атаки (fake server/offer flood).
- Требуются права root для L2‑инъекций.

### 2. ntlmrelayx — релей на LDAP
```bash
ntlmrelayx.py -t ldap://dc01.lab.local --add-computer
```
- **`-t ldap://...`** — цель релея (LDAP на DC).
- **`--add-computer`** — попытка создать машинный аккаунт в домене от имени жертвы.

### 3. ntlmrelayx — релей на SMB (пример)
```bash
ntlmrelayx.py -t smb://filesrv.lab.local --dump-sam
```
- **`--dump-sam`** — выгрузка локальной SAM на целевом сервере при успешном реле.
