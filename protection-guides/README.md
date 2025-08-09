# Protection Guides — Руководства по защите и противодействию NTLM Relay

Данный раздел репозитория содержит практические материалы по защите инфраструктуры Active Directory от атак типа **NTLM Relay**, а также рекомендации по мониторингу и выявлению подобных атак с помощью SIEM.

## 📂 Структура

### 📁 checklist
- [NTLM_Relay_Checklist.md](./checklist/NTLM_Relay_Checklist.md) — пошаговый чек-лист по защите от NTLM Relay, включая сетевые, протокольные и организационные меры.

### 📁 scheme
- [NTLM_Relay_Scheme.png](./scheme/NTLM_Relay_Scheme.png) — наглядная схема атаки NTLM Relay.
- [NTLM_Relay_Scheme_source.drawio](./scheme/NTLM_Relay_Scheme_source.drawio) — исходник схемы для редактирования в draw.io/diagrams.net.

### 📁 siem
- [SIEM_monitoring_recommendations.md](./siem/SIEM_monitoring_recommendations.md) — рекомендации по настройке правил корреляции и мониторингу в SIEM для детектирования NTLM Relay и смежных техник.

### 📁 tools
- [responder_usage.md](./tools/responder_usage.md) — примеры работы с инструментом Responder (перехват NTLM-хэшей через LLMNR/NBT-NS/WPAD).
- [impacket_usage.md](./tools/impacket_usage.md) — примеры и сценарии использования Impacket (Pass-the-Hash, SMB/LDAP Relay, Zerologon).
- [psexec_examples.md](./tools/psexec_examples.md) — наглядная таблица использования `psexec.py` для аутентификации через NTLM-хэши.

## 🎯 Цели
- Повысить осведомлённость команды ИБ о векторах атак на основе NTLM Relay.
- Предоставить готовые инструкции и схемы для обучения и тестирования в лаборатории.
- Сформировать базовый набор правил для SIEM с учётом специфики инфраструктуры.

## 🛡 Рекомендуемое применение
1. Использовать [NTLM_Relay_Checklist.md](./checklist/NTLM_Relay_Checklist.md) для аудита текущей инфраструктуры.
2. Развернуть в тестовой среде сценарии из [responder_usage.md](./tools/responder_usage.md) и [impacket_usage.md](./tools/impacket_usage.md) для практического понимания работы инструментов.
3. Внедрить правила из [SIEM_monitoring_recommendations.md](./siem/SIEM_monitoring_recommendations.md) в существующую SIEM и протестировать детектирование.
4. Проводить обучение ИТ и ИБ персонала с использованием [NTLM_Relay_Scheme.png](./scheme/NTLM_Relay_Scheme.png).

## 📜 Лицензия
Материалы предоставляются для учебных и тестовых целей. Использование в продуктивной среде — на усмотрение владельца инфраструктуры.
