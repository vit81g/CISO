# BloodHound — анализ привилегий в Active Directory

Официальный сайт: [https://bloodhound.readthedocs.io/](https://bloodhound.readthedocs.io/)

## 📦 Установка

### 1. Установка Neo4j
```bash
sudo apt update
sudo apt install neo4j
sudo neo4j console
```
Откройте [http://localhost:7474](http://localhost:7474) и установите пароль для пользователя `neo4j`.

### 2. Установка BloodHound
Скачайте релиз с GitHub:
```bash
wget https://github.com/BloodHoundAD/BloodHound/releases/latest/download/BloodHound-linux-x64.zip
unzip BloodHound-linux-x64.zip
cd BloodHound-linux-x64
./BloodHound --no-sandbox
```

### 3. Сбор данных SharpHound
Скачайте SharpHound:
```bash
wget https://github.com/BloodHoundAD/SharpHound/releases/latest/download/SharpHound.exe
```
Запустите на машине в домене:
```powershell
SharpHound.exe -c All
```
Импортируйте полученные данные `.zip` в BloodHound.

## 🔹 Примеры использования
- Построить граф всех админских связей.
- Найти путь от пользователя до Domain Admin.

## 🛡 Защита
- Ограничить доступ к LDAP.
- Мониторить массовые LDAP-запросы.
