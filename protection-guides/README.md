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
- [AD Trusts Attack Paths (BloodHound) — эксплуатация trust-отношений AD для междоменного компромисса.
- [BadSuccessor — Эскалация через dMSA](./attacks/badsuccessor-abuse-dmsa.md) — подмена свойств dMSA для получения привилегий домена.
- [CVE-2025-21293 — Privilege Escalation в AD DS](./attacks/cve-2025-21293-priv-esc.md) — эксплуатация уязвимости в Active Directory Domain Services для повышения привилегий.
- [DHCP Spoofing](./attacks/dhcp-spoofing_attack.md) — подмена параметров DHCP для перехвата трафика или атак relay.
- [Entra ID Sync Abuse](./attacks/entra-id-sync-abuse.md) — злоупотребление синхронизацией Entra ID для компрометации учетных данных.
- [Golden dMSA Attack](./attacks/golden-dmsa-attack.md) — кросс-доменная атака через подбор пароля dMSA для персистентного доступа.
- [Hybrid AD Authentication Bypass](./attacks/hybrid-ad-authentication-bypass.md) — обход аутентификации в гибридном AD с Entra ID.
- [IPv6 Relay (MITM6) — MITM-атака через IPv6 для перехвата NTLM.
- [Kerberoasting (Updated) — кража и оффлайн-взлом тикетов Kerberos для gMSA.
- [LDAP DoS Attack](./attacks/ldap-dos-attack.md) — перегрузка службы LDAP для отказа в обслуживании AD.
- [LLMNR Poisoning (Updated) — отравление LLMNR для кражи NTLM-хэшей.
- [MSSQL / HTTP Relay Attack](./attacks/mssql-http-relay_attack.md) — релей аутентификации через MSSQL или HTTP для эскалации привилегий.
- [NTLM Relay Attack](./attacks/ntlm-relay_attack.md) — релей NTLM-аутентификации для выполнения команд от имени пользователя.
- [Pass-the-Hash](./attacks/pass-the-hash.md) — использование NTLM-хэша вместо пароля для аутентификации.
- [PrinterBug Attack](./attacks/printerbug_attack.md) — эксплуатация MS-RPRN для вызова аутентификации с целевого хоста.
- [SMB Relay (Updated) — релей SMB-сессий для выполнения кода.
- [Zerologon Attack](./attacks/zerologon_attack.md) — эксплуатация CVE-2020-1472 для полного захвата контроллера домена.

### 📁 Защита
- [AD Hardening](./protection/hardening-active-directory.md) — усиление безопасности Active Directory.
- [SMB/LDAP Hardening](./protection/hardening-smb-ldap.md) — защита SMB и LDAP.
- [DHCP/DNS Security](./protection/hardening-dhcp-dns.md) — защита служб DHCP и DNS.
- [Endpoint Hardening](./protection/hardening-endpoints.md) — защита конечных точек.
- [Network Segmentation](./protection/network-segmentation.md) — сегментация сети.

### 📁 playbooks
- [General Incident Response](./playbooks/general-incident-response.md) — общий план реагирования на инциденты ИБ.
- [NTLM Relay Response](./playbooks/ntlm-relay-response.md) — реагирование на атаку NTLM Relay.
- [AD dMSA Compromise](./playbooks/playbook-ad-dmsa-compromise.md) — реагирование на компрометацию dMSA.
- [AD Trusts Abuse](./playbooks/playbook-ad-trusts-abuse.md) — реагирование на злоупотребление trust-отношениями AD.
- [Hybrid AD Bypass](./playbooks/playbook-hybrid-ad-bypass.md) — реагирование на обход аутентификации в гибридном AD.
- [Kerberoasting gMSA](./playbooks/playbook-kerberoasting-gmsa.md) — реагирование на атаку Kerberoasting против gMSA.
- [NTLM Relay](./playbooks/playbook-ntlm-relay.md) — план реагирования на NTLM Relay (детализированный).

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