# IPv6 Relay (MITM6) — MITM Attack for NTLM Theft

**Предупреждение:** Используйте только в авторизованных тестах.

## 🎯 Цель атаки
MITM через IPv6 для перехвата NTLM в hybrid AD.

## 📋 Условия
- IPv6 enabled по умолчанию.
- Нет IPv6 security.

## 🔹 Почему Это Работает
Spoof DHCPv6; перенаправить трафик; capture NTLM.

## 🔹 Пошагово
1. mitm6 -d domain.local.
2. Комбо с Responder для relay.

**Потенциальная ошибка:** IPv6 disabled — no effect.

## 📊 SIEM
- DHCPv6 logs; unexpected IPv6 assigns.

## 🛡 Защита
- Disable IPv6 if unused.
- DHCPv6 Guard.

## 📌 Вариации
- Комбо с WPAD для proxy MITM.
