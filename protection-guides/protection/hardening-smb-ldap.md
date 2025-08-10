# Hardening SMB/LDAP (Updated for 2025)

## 🎯 Цели
Защитить SMB и LDAP протоколы в среде Active Directory от атак: **SMB Relay Updated**, **IPv6 Relay (MITM6)**, **LLMNR Poisoning Updated**.

## ⚠ Угрозы
- Перехват и релей NTLM-аутентификации через SMB (SMB Relay).
- Эксплуатация автоконфигурации IPv6 для MITM и релея на LDAP (IPv6 Relay).
- Перехват хэшей через LLMNR/NBT-NS и их релей на SMB/LDAP.

## 🛡 Меры защиты
### 1. SMB Signing и NTLM
- Включить SMB signing на всех серверах и клиентах.  
  **MITRE ATT&CK:** T1021.002 (SMB/Windows Admin Shares)
- Запретить использование NTLM, перейти на Kerberos.
- Настроить политики:
```powershell
Set-SmbServerConfiguration -EnableSecuritySignature $true
Set-SmbClientConfiguration -EnableSecuritySignature $true
```

### 2. LDAP Signing и Channel Binding
- Включить LDAP signing и channel binding.  
  **MITRE ATT&CK:** T1557.001 (LLMNR/NBT-NS Poisoning)
- GPO: **Domain Controller: LDAP server signing requirements** → Require signing.

### 3. IPv6 и WPAD
- Отключить IPv6, если не используется.
- Запретить WPAD через GPO:  
  **Administrative Templates → Network → Network Connections → WPAD**.

### 4. LLMNR/NBT-NS
- Отключить LLMNR и NBT-NS через GPO:
```
Computer Configuration → Administrative Templates → Network → DNS Client → Turn Off Multicast Name Resolution → Enabled
```

### 5. Мониторинг
- Event ID 4624 (Logon Type 3) с нетипичных IP.
- NTLM входы без SMB signing.

## ⚙ Настройка
### Проверка SMB Signing
```powershell
Get-SmbServerConfiguration | Select EnableSecuritySignature
```
### Отключение LLMNR
```powershell
reg add "HKLM\Software\Policies\Microsoft\Windows NT\DNSClient" /v EnableMulticast /t REG_DWORD /d 0 /f
```

## 📌 Дополнительно
- **MITRE ATT&CK:** T1021.002, T1557.001  
- [Microsoft: SMB Security](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-security)  
- [LDAP Signing and Channel Binding](https://learn.microsoft.com/en-us/windows-server/identity/ldap/ldap-signing)  
