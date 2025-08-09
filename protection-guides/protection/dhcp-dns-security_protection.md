# DHCP/DNS Security

## 🎯 Цель
Защита инфраструктуры DHCP и DNS от подмены и атак типа DHCP Spoofing.

## 🔹 Меры защиты
- Включить DHCP Snooping на коммутаторах.
- Включить Dynamic ARP Inspection (DAI).
- Применить IP Source Guard.
- Жёстко задавать DNS через GPO.
- Запретить WPAD.
- Ограничить DHCP-сервера списком авторизованных в AD.

## 📊 Мониторинг
- DHCP Snooping violations.
- Изменение DNS-серверов на хостах.
