# LLMNR Poisoning — Credential Theft in Hybrid AD

**Предупреждение:** Используйте только в авторизованных тестах.

## 🎯 Цель атаки
Перехват хэшей через отравление LLMNR для входа в hybrid AD.

## 📋 Условия
- LLMNR/NBT-NS enabled.
- Hybrid среда.

## 🔹 Почему Это Работает
Отравление name resolution; машины шлют хэши атакующему.

## 🔹 Пошагово
1. Responder: sudo responder -I eth0.
2. Ждать запросов; crack хэши (hashcat).

## 📊 SIEM
- Event ID 4624 с unexpected IP.

## 🛡 Защита
- Disable LLMNR/NBT-NS.
- Strong passwords.

## 📌 Вариации
- Комбо с IPv6.
