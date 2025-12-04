# T1036 Masquerading — папка `scripts`

Папка предназначена для хранения скриптов и одноразовых команд PowerShell, использованных при расследовании инцидента с подменой процесса `csrss.exe`.

На текущий момент скрипты оформлены в виде набора команд, которые можно сохранить в `.ps1`‑файлы при необходимости автоматизации.

## Базовый набор команд

```powershell
# 1. Переход на диск C: удалённого хоста
cd \\host_name\c$\

# 2. Просмотр содержимого Program Files (x86), включая скрытые элементы
Get-ChildItem -Path "\\host_name\c$\Program Files (x86)" -Force

# 3. Отбор только скрытых файлов и каталогов
Get-ChildItem -Path "\\host_name\c$\Program Files (x86)" -Force |
    Where-Object { $_.Attributes -match "Hidden" }

# 4. Получение SHA256-хэша подозрительного файла
Get-FileHash "\\host_name\c$\Program Files (x86)\csrss\csrss2\csrss.exe" -Algorithm SHA256

# 5. Проверка цифровой подписи файла
Get-AuthenticodeSignature "\\host_name\c$\Program Files (x86)\csrss\csrss2\csrss.exe"

# 6. Получение полной информации о сертификате
(Get-AuthenticodeSignature "\\host_name\c$\Program Files (x86)\csrss\csrss2\csrss.exe").SignerCertificate |
    Format-List *
```

## Варианты автоматизации

Рекомендуется со временем вынести команды в отдельные скрипты, например:

- `01_enum_hidden_csrss.ps1` — поиск скрытых каталогов `csrss` и вывод их атрибутов;
- `02_get_csrss_hash.ps1` — вычисление хэша файла и экспорт в CSV;
- `03_get_csrss_signature.ps1` — проверка подписи и экспорта информации о сертификате.

Такой подход позволит быстро переиспользовать одно и то же расследование на других хостах.
