# DHCP Spoofing — подмена параметров сети

## 🎯 Цель атаки
Направить трафик клиента через атакующего (MITM), подменив DNS/WPAD/Gateway.

## 📋 Условия
- Нет DHCP Snooping.
- Клиент принимает конфигурацию от любого DHCP-сервера.

## 🔹 Пошагово
1. Запустить DHCP spoofing:
```bash
yersinia -I
```
2. Назначить поддельный DNS или WPAD.
3. Клиенты начнут отправлять NTLM на атакующего (связка с Responder/ntlmrelayx).

## 📊 SIEM
- Изменение DNS/шлюза в логах клиента.
- DHCP Snooping violation (если включен).

## 🛡 Защита
- Включить DHCP Snooping, DAI.
- Жёстко задавать DNS через GPO.
