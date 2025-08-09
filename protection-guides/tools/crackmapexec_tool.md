# CrackMapExec — автоматизация атак на SMB, WinRM, RDP

## 📦 Установка
```bash
sudo apt update
sudo apt install crackmapexec
```

## 🔹 Примеры использования
1. Проверка NTLM-хэша:
```bash
crackmapexec smb 192.168.0.0/24 -u admin -H <NT_hash>
```
2. Выполнение команды через SMB:
```bash
crackmapexec smb target -u user -p pass -x "ipconfig"
```

## 📋 Описание
Позволяет массово проверять учётки и выполнять команды через SMB, WinRM и RDP.

## 🛡 Защита
- Ограничить доступ к SMB, WinRM, RDP.
- Включить MFA для RDP.
