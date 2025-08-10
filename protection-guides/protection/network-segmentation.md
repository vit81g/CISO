# Network Segmentation (Updated for 2025)

## 🎯 Цели
Ограничить латеральное перемещение и воздействие атак, изолируя критичные роли: DC, серверы синхронизации Entra Connect, базы данных, админские рабочие места (PAW).

## ⚠ Угрозы
- **AD Trusts Attack Paths** — междоменный/межлесной переход.  
- **SMB/LDAP Relay** — релеи в пределах широких L2 доменов.  
- **Hybrid AD Bypass** — доступ к Sync/ADSync DB из пользовательских VLAN.

## 🛡 Меры защиты
### 1) Сегментация по ролям
- Выделенные VLAN/сегменты: **DC**, **Sync (Entra Connect)**, **SQL/ADSync DB**, **Admin PAW**, **User**.  
  **MITRE ATT&CK:** T1021 (Remote Services), T1078 (Valid Accounts)
- East‑West ACL: запрет SMB/LDAP/ RPC между User ↔ Server/Sync; разрешать строго по списку.

### 2) Контроль периметра сегментов
- Межсетевой экран L3/L7 с правилами «по умолчанию запрещено».  
- IDS/IPS/NSM для межсегментного трафика (сигнатуры SMB/LDAP relay).

### 3) Jump/PAW
- Все админ‑операции только с **PAW** в админском сегменте.  
- Блок RDP/WinRM/SMB к DC из User‑VLAN.  
  **MITRE ATT&CK:** T1021.001/002, T1078

### 4) IPv6/WPAD
- Блок RA/DHCPv6 из пользовательских VLAN (RA/DHCPv6 Guard).  
- Запрет WPAD трафика между сегментами.

### 5) Мониторинг
- Логи межсетевых экранов: попытки доступа к портам 88/135/389/445/636/3268/9389 между сегментами.  
- Корреляции «неадминский сегмент → админские сервисы» (в т.ч. IPv6).

## ⚙ Настройка (примеры)
### Пример ACL (высокоуровневый)
```
deny  user_vlan  -> dc_vlan      tcp 88,135,389,445,636,3268,9389
deny  user_vlan  -> sync_vlan    any
permit paw_vlan  -> dc_vlan      tcp 88,135,389,445,636,3268,9389
deny  any        -> wpad_host    tcp 80,443
```
### Ограничение админ‑доступов
- Использовать **Privileged Access Workstations (PAW)** и jump‑host.

## 📌 Дополнительно
- **MITRE ATT&CK:** T1021, T1078, T1557  
- Microsoft ESAE/PAW, CIS Controls: Network Segmentation
