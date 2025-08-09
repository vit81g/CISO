# Responder — захват хэшей через LLMNR и NBT-NS

## 📦 Установка
```bash
sudo apt update
sudo apt install responder
```

## 🔹 Примеры использования
1. Запуск Responder на интерфейсе eth0:
```bash
sudo responder -I eth0
```
2. Логирование в отдельный файл:
```bash
sudo responder -I eth0 -w -F -v
```

## 📋 Описание
**Responder** перехватывает NTLM/NetNTLMv2-хэши через протоколы LLMNR, NBT-NS и WPAD.

## 📊 SIEM
- NTLM-аутентикация на неожиданные хосты.
- DNS/LLMNR/NBT-NS-запросы к несуществующим именам.

## 🛡 Защита
- Отключить LLMNR и NBT-NS.
- Отключить WPAD.
