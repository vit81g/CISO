# Hardening DHCP/DNS (Updated for 2025)

## 🎯 Цели
Предотвратить атаки **MITM6 (IPv6 Relay)** и **LLMNR Poisoning**, минимизировать вероятность выдачи клиентам поддельных сетевых параметров (DNS/WPAD/Gateway).

## ⚠ Угрозы
- Подмена параметров через DHCPv4/v6 и RA (Router Advertisement) → перехват NTLM.
- Резервные механизмы разрешения имён (LLMNR/NBT-NS) → утечка хэшей.

## 🛡 Меры защиты
### 1) Сетевые контроли L2/L3
- **DHCP Snooping** на всех не‑трастовых портах (mark trusted только аплинки/DHCP).  
- **Dynamic ARP Inspection (DAI)** и **IP Source Guard** на пользовательских VLAN.  
- **RA Guard** и **DHCPv6 Guard** для IPv6.  
  **MITRE ATT&CK:** T1557 (Adversary-in-the-Middle)

### 2) DNS и WPAD
- Жёстко задавать DNS через GPO/статически; запретить WPAD.  
- Заблокировать `wpad.*` записи в DNS/зоне, создать заглушку A-запись на 0.0.0.0.  
  **MITRE ATT&CK:** T1557.001 (LLMNR/NBT-NS Poisoning)

### 3) Отключение LLMNR/NBT‑NS
- GPO: **Turn off Multicast Name Resolution** → Enabled.  
- Отключить NetBIOS over TCP/IP там, где возможно.  
  **MITRE ATT&CK:** T1557.001

### 4) Защита DHCP‑инфраструктуры
- Авторизовать DHCP‑серверы в AD.  
- Разнести DHCP/DNS/AD DS по разным VLAN, ограничить доступ ACL.  
- Логирование DHCP (аудит lease/offer/decline).

### 5) Мониторинг
- Аномалии выдачи DHCP‑адресов, множественные **DORA** от одного MAC.  
- Новые RA/DHCPv6 объявления в пользовательских VLAN.  
- NXDOMAIN всплески и обращения к `wpad`/рандомным именам.

## ⚙ Настройка (примеры)
### Cisco IOS — DHCP Snooping/DAI/IPSG
```
ip dhcp snooping
ip dhcp snooping vlan 10,20
interface range Gi1/0/1-48
  ip dhcp snooping limit rate 30
  ip arp inspection trust
!
ip arp inspection vlan 10,20
ip verify source vlan dhcp-snooping
```
### Отключение LLMNR через GPO
```
Computer Configuration → Administrative Templates → Network → DNS Client →
"Turn Off Multicast Name Resolution" = Enabled
```

## 📌 Дополнительно
- **MITRE ATT&CK:** T1557, T1557.001  
- Microsoft, Cisco: DHCP Snooping / RA Guard / DHCPv6 Guard / IPSG best practices
