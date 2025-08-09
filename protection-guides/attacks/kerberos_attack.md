# Kerberos — атаки на аутентификацию в AD

## 🎯 Цель атаки
Получить Kerberos Ticket Granting Service (TGS) или Ticket Granting Ticket (TGT) для последующего взлома оффлайн.

## 📋 Техники
- **Kerberoasting** — запрос TGS для сервисного аккаунта и взлом оффлайн.
- **AS-REP Roasting** — запрос AS-REP для аккаунта без pre-auth.
- **Pass-the-Ticket** — использование украденного TGT/TGS.

## 🔹 Пошагово (Kerberoasting)
1. Запросить TGS для сервисного аккаунта:
```bash
GetUserSPNs.py domain.local/user:password
```
2. Взломать хэш оффлайн:
```bash
hashcat -m 13100 hash.txt wordlist.txt
```

## 📊 SIEM
- Event ID 4769 — Kerberos service ticket request.
- Необычное количество запросов TGS.

## 🛡 Защита
- Сложные пароли для сервисных аккаунтов.
- Запрет DES/RC4.
- Мониторинг 4769 на массовые запросы.
