# Protection Guides — Руководства по защите и противодействию NTLM Relay

Данный раздел репозитория содержит практические материалы по защите инфраструктуры Active Directory от атак типа **NTLM Relay**, а также рекомендации по мониторингу и выявлению подобных атак с помощью SIEM.

---

## 📌 Схема атаки
![NTLM Relay Scheme](./scheme/NTLM_Relay_Scheme.png)

---

## 📂 Структура

### 📁 checklist
- [NTLM_Relay_Checklist.md](./checklist/NTLM_Relay_Checklist.md) — пошаговый чек-лист по защите от NTLM Relay.

### 📁 scheme
- [NTLM_Relay_Scheme.png](./scheme/NTLM_Relay_Scheme.png) — наглядная схема атаки NTLM Relay.
- [NTLM_Relay_Scheme_source.drawio](./scheme/NTLM_Relay_Scheme_source.drawio) — исходник схемы для редактирования в draw.io/diagrams.net.

### 📁 siem
- [SIEM_monitoring_recommendations.md](./siem/SIEM_monitoring_recommendations.md) — рекомендации по настройке правил корреляции и мониторингу.

### 📁 tools
- [responder_usage.md](./tools/responder_usage.md) — гайд по Responder (перехват NTLM-хэшей).
- [impacket_usage.md](./tools/impacket_usage.md) — гайд по Impacket (Pass-the-Hash, SMB/LDAP Relay, Zerologon).
- [psexec_examples.md](./tools/psexec_examples.md) — примеры использования `psexec.py`.

### 📁 attacks
- [NTLM Relay](./attacks/ntlm-relay_attack.md) — релей NTLM-аутентификации.
- [Kerberos](./attacks/kerberos_attack.md) — атаки на Kerberos (Kerberoasting, AS-REP Roasting, Pass-the-Ticket).
- [DHCP Spoofing](./attacks/dhcp-spoofing_attack.md) — подмена параметров сети.
- [Zerologon](./attacks/zerologon_attack.md) — эксплуатация CVE-2020-1472.
- [PrinterBug](./attacks/printerbug_attack.md) — эксплуатация MS-RPRN.

### 📁 protection
- [AD Hardening](./protection/ad-hardening_protection.md) — усиление безопасности Active Directory.
- [SMB/LDAP Hardening](./protection/smb-ldap-hardening_protection.md) — защита SMB и LDAP.
- [DHCP/DNS Security](./protection/dhcp-dns-security_protection.md) — защита служб DHCP и DNS.
- [Endpoint Hardening](./protection/endpoint-hardening_protection.md) — защита конечных точек.
- [Network Segmentation](./protection/network-segmentation_protection.md) — сегментация сети.

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
