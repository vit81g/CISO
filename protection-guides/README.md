# Protection Guides — Комплексные меры защиты AD и сетевой инфраструктуры

Данный раздел репозитория содержит практические материалы по защите инфраструктуры Active Directory от актуальных техник атак (включая NTLM Relay, релей SMB/LDAP/HTTP, атаки на Kerberos, dMSA/gMSA, Zerologon и др.), а также рекомендации по мониторингу и выявлению подобных действий с помощью SIEM.

---

## 📌 Схема атаки
![AD Attack–Defense Map](./scheme/ad_attack_defense_map.png)
[Источник схемы (.drawio)](./scheme/ad_attack_defense_map.drawio)

![NTLM Relay Scheme](./scheme/NTLM_Relay_Scheme.png)

---

## 📂 Структура

### 📁 Чек-лист
- [NTLM_Relay_Checklist.md](./checklist/NTLM_Relay_Checklist.md) — пошаговый чек-лист по защите от NTLM Relay.

### 📁 Схема
- [NTLM_Relay_Scheme.png](./scheme/NTLM_Relay_Scheme.png) — наглядная схема атаки NTLM Relay.
- [NTLM_Relay_Scheme_source.drawio](./scheme/NTLM_Relay_Scheme_source.drawio) — исходник схемы для редактирования в draw.io/diagrams.net.

### 📁 SIEM
- [SIEM_monitoring_recommendations.md](./siem/SIEM_monitoring_recommendations.md) — рекомендации по настройке правил корреляции и мониторингу.

### 📁 Инструменты
- [BloodHound](./tools/bloodhound_tool.md)
- [CrackMapExec](./tools/crackmapexec_tool.md)
- [Impacket](./tools/impacket_usage.md)
- [Mimikatz / pypykatz](./tools/mimikatz_tool.md)
- [MITM6](./tools/mitm6_tool.md)
- [psexec (Примеры)](./tools/psexec_examples.md)
- [Responder](./tools/responder_usage.md)
- [SharpHound](./tools/sharphound_tool.md)

### 📁 Реализация атак
- [AD Trusts Attack Paths (BloodHound)](./attacks/ad-trusts-attack-paths-bloodhound.md)
- [BadSuccessor — Эскалация через dMSA](./attacks/badsuccessor-abuse-dmsa.md)
- [CVE-2025-21293 — Privilege Escalation в AD DS](./attacks/cve-2025-21293-priv-esc.md)
- [DHCP Spoofing](./attacks/dhcp-spoofing_attack.md)
- [Entra ID Sync Abuse](./attacks/entra-id-sync-abuse.md)
- [Golden dMSA Attack](./attacks/golden-dmsa-attack.md)
- [Hybrid AD Authentication Bypass](./attacks/hybrid-ad-authentication-bypass.md)
- [IPv6 Relay (MITM6)](./attacks/ipv6-relay-mitm6.md)
- [Kerberoasting (Updated)](./attacks/kerberoasting-updated.md)
- [LDAP DoS Attack](./attacks/ldap-dos-attack.md)
- [LLMNR Poisoning (Updated)](./attacks/llmnr-poisoning-updated.md)
- [MSSQL / HTTP Relay Attack](./attacks/mssql-http-relay_attack.md)
- [NTLM Relay Attack](./attacks/ntlm-relay_attack.md)
- [Pass-the-Hash](./attacks/pass-the-hash.md)
- [PrinterBug Attack](./attacks/printerbug_attack.md)
- [SMB Relay (Updated)](./attacks/smb-relay-updated.md)
- [Zerologon Attack](./attacks/zerologon_attack.md)

### 📁 Защита
- [AD Hardening](./protection/hardening-active-directory.md) — усиление безопасности Active Directory.
- [SMB/LDAP Hardening](./protection/hardening-smb-ldap.md) — защита SMB и LDAP.
- [DHCP/DNS Security](./protection/hardening-dhcp-dns.md) — защита служб DHCP и DNS.
- [Endpoint Hardening](./protection/hardening-endpoints.md) — защита конечных точек.
- [Network Segmentation](./protection/network-segmentation.md) — сегментация сети.

### 📁 playbooks
- [ntlm-relay-response.md](./playbooks/ntlm-relay-response.md) — реагирование на NTLM Relay.
- [general-incident-response.md](./playbooks/general-incident-response.md) — универсальный план реагирования.

---

## 🎯 Цели
- Повысить осведомлённость команды ИБ о векторах атак на основе NTLM Relay и смежных техник.
- Предоставить готовые инструкции и схемы для обучения и тестирования.
- Сформировать набор правил для SIEM под инфраструктуру организации.

## 🛡 Рекомендуемое применение
1. Использовать [NTLM_Relay_Checklist.md](./checklist/NTLM_Relay_Checklist.md) для аудита.
2. Запустить сценарии из [tools](./tools) в тестовой среде.
3. Внедрить правила из [siem](./siem) в боевую SIEM.
4. Проводить обучение с использованием схем и материалов из [attacks](./attacks).

## 📜 Лицензия
Материалы предоставляются для учебных и тестовых целей. Использование в продуктивной среде — на усмотрение владельца инфраструктуры.
