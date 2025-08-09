# SharpHound — сбор данных для BloodHound

## 📦 Установка
Скачайте с GitHub:
```bash
wget https://github.com/BloodHoundAD/SharpHound/releases/latest/download/SharpHound.exe
```

## 🔹 Примеры использования
1. Сбор всех данных:
```powershell
SharpHound.exe -c All
```
2. Сбор только сессий входа:
```powershell
SharpHound.exe -c Session
```

## 🛡 Защита
- Ограничить доступ к LDAP.
- Мониторить массовые запросы.
