# Kerberoasting (Updated) — Offline Cracking of Service Accounts

**Предупреждение:** Используйте только в авторизованных тестах.

## 🎯 Цель атаки
Кракинг TGS сервис-аккаунтов оффлайн; фокус на gMSA в 2025.

## 📋 Условия
- SPN на аккаунтах с weak passwords.
- Доступ к домену.

## 🔹 Почему Это Работает
Запрос TGS; хэш шифрован паролем; crack оффлайн.

## 🔹 Пошагово
1. GetUserSPNs.py domain/user.
2. Hashcat -m 13100 hash.txt rockyou.txt.

**Потенциальная ошибка:** AES enabled — use -m 19700.

## 📊 SIEM
- Event ID 4769; high volume requests.

## 🛡 Защита
- Strong passwords; monitor 4769.

## 📌 Вариации
- Target gMSA; комбо с Golden dMSA.
