
## golden_dmsa_attack.md
```markdown
# Golden dMSA — Cross-Domain Attack via dMSA Password Brute-Force

**Предупреждение:** Используйте только в авторизованных тестах. Крипто-уязвимость в WS2025.

## 🎯 Цель атаки
Кросс-доменная латеральная атака и персистентный доступ ко всем managed service accounts в AD.

## 📋 Условия
- dMSA в Windows Server 2025.
- Доступ к крипто-структурам (ManagedPasswordId).

## 🔹 Почему Это Работает
ManagedPasswordId предсказуем (time-based, 1024 комбинации); brute-force генерирует пароли dMSA.

## 🔹 Пошагово
1. Захватить ManagedPasswordId из AD.
2. Brute-force пароли (инструмент GoldenDMSA).
3. Генерировать пароли для dMSA; аутентифицироваться кросс-домен.

**Потенциальная ошибка:** "Invalid Password" — неверный brute-force.

## 📊 SIEM
- Аномальные доступы к dMSA (Event ID 4624 с unexpected source).
- **Sigma Rule:** detection: EventID: 4624 AND AccountName: *dMSA*

## 🛡 Защита
- Аудит dMSA; ротация ключей.
- Патч от Microsoft (July 2025).

## 📌 Вариации
- Интеграция с BadSuccessor для эскалации.
