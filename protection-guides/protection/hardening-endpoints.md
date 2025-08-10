# Hardening Endpoints (Updated for 2025)

## 🎯 Цели
Снизить риск компрометации рабочих станций/серверов и предотвратить техники: **Pass‑the‑Hash**, **Kerberoasting (gMSA)**, **LLMNR Poisoning**, **SMB Relay**.

## ⚠ Угрозы
- Извлечение секретов из LSASS (пароли/хэши/билеты).  
- Неавторизованные NTLM/SMB/LDAP сессии.  
- Резервное разрешение имён (LLMNR/NBT‑NS).

## 🛡 Меры защиты
### 1) Память и учётные данные
- Включить **Credential Guard** / **LSA Protection** (`RunAsPPL`).  
  **MITRE ATT&CK:** T1003.001/T1003.006 (OS Credential Dumping)
- Запрет неинтерактивного кеширования паролей локально (по ролям).
- WDAC/AppLocker для ограничения запуска посторонних утилит (mimikatz/pypykatz).

### 2) Аутентификация и протоколы
- Отключить **NTLM** там, где возможно; принудить Kerberos.  
- Включить **SMB signing** на клиентах.  
- Отключить **SMBv1**.  
  **MITRE ATT&CK:** T1550.002 (Use of Hash), T1021.002 (SMB)

### 3) Разрешение имён
- Отключить **LLMNR/NBT‑NS** (GPO/реестр), запретить WPAD.  
  **MITRE ATT&CK:** T1557.001

### 4) Учётные записи и привилегии
- Локальные администраторы: минимальный состав, использовать **LAPS**/**Windows LAPS**.  
- Разделение админских учёток (Tiering), запрет интерактивного входа админов на user‑хосты.

### 5) Мониторинг/EDR
- Включить Sysmon: правила на доступ к **lsass.exe**, создание dump‑файлов, загрузка известных инструментов.  
- Контроль Event ID: **4624/4625**, **4672**, **4688**, **10 (Sysmon)**.

## ⚙ Настройка (примеры)
### Включение LSA Protection
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "RunAsPPL" -Value 1 -PropertyType DWord -Force
```
### SMB signing на клиенте
```powershell
Set-SmbClientConfiguration -EnableSecuritySignature $true -RequireSecuritySignature $true
```

## 📌 Дополнительно
- **MITRE ATT&CK:** T1003.001, T1003.006, T1550.002, T1021.002, T1557.001  
- Microsoft: Credential Guard / LAPS / Windows LAPS
