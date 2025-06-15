# Практические задания по дням

> Эти задания предназначены для выполнения в Kali Linux VM. Некоторые требуют Wireshark, Nmap, Bettercap, Zeek и других инструментов. Указаны ссылки на `.pcap`-файлы для анализа, а также примеры команд.

---

## День 1. Подготовка среды

* Установить Kali Linux VM (2 CPU, 4 GB RAM).
* Обновить систему: `sudo apt update && sudo apt full-upgrade -y`
* Настроить SSH (опционально – через ключи).
* Снять снапшот: **clean-base**.

---

## День 2. TCP-трафик в Wireshark

**Задание:**

1. Запустить HTTP-сервер:

```bash
python3 -m http.server 8080 &
curl http://127.0.0.1:8080
```

2. Записать трафик Wireshark (`lo` интерфейс).
3. Сохранить `day02_handshake.pcap`, отметить тройное рукопожатие.

---

## День 3. ARP и ICMP

**Задание:**

1. Выполнить `ping` шлюза (например `ping -c 4 192.168.56.1`).
2. Сохранить захват `ping.pcap`.
3. Выполнить `ip neigh > arp_cache.txt` и приложить файл.

**Примерный pcap (альтернатива):**

* [arp-storm.pcap](https://gitlab.com/wireshark/wireshark/-/raw/master/samplecaptures/arp-storm.pcap)

---

## День 4. Субнеттинг

**Задание:**

1. Разбить 172.16.0.0/16 на подсети: 1000, 500, 200, 100, 50 хостов.
2. Составить таблицу: Network, Netmask, Hosts, Broadcast.

Инструмент: `ipcalc` или [https://www.subnet-calculator.com/](https://www.subnet-calculator.com/)

---

## День 5. DHCP и NAT

**Задание:**

1. Запустить DHCP-клиент: `sudo dhclient -v eth0`
2. Захватить трафик (`port 67 or 68`).
3. Сравнить внешний IP: `curl ifconfig.me`

Примерный pcap:

* [dhcp.pcap](https://gitlab.com/wireshark/wireshark/-/raw/master/samplecaptures/dhcp.pcap)

---

## День 6. Сканирование сети (Nmap)

**Задание:**

1. `sudo nmap -sn 192.168.56.0/24 -oN hosts.txt`
2. Скан портов: `sudo nmap -sS -p1-1000 -iL hosts.txt -oN ports.txt`
3. Сформировать таблицу IP ↔ открытые порты.

---

## День 7. NSE и уязвимости

**Задание:**

1. Скан конкретного IP:

```bash
sudo nmap -sV --script=http-enum,vulners -p80,443 <target-IP> -oN vulns.txt
```

2. Найти CVE с высоким рейтингом.

---

## День 8. IDS и обход

**Задание:**

1. Выполнить обычный `nmap -sS -O`.
2. Затем: `nmap -sS -O --data-length 120 --source-port 53 <target-IP>`
3. Сравнить трафик (Wireshark): `normal_vs_stealth.pcap`.

---

## День 9. Уязвимости в GVM (OpenVAS)

**Задание:**

1. Установить: `sudo gvm-setup && gvm-check-setup`
2. Сканировать Kali или другую VM.
3. Экспорт отчёта в PDF, отметить 3 уязвимости (CVSS > 7).

---

## День 10. MITM в локальной сети

**Задание:**

```bash
sudo bettercap -iface eth0
> set arp.spoof.targets <victim>
> arp.spoof on
> net.sniff on
```

Сохранить перехваченный HTTP cookie (pcap + screenshot).

---

## День 11. WPA2 PSK взлом

**Пример pcap:**

* [wpa-Induction.pcap](https://gitlab.com/wireshark/wireshark/-/raw/master/samplecaptures/wpa-Induction.pcap)

**Задание:**

```bash
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b <BSSID> handshake.pcap
```

Сохранить найденный пароль.

---

## День 12. Дешифровка TLS-трафика

**Пример pcap:**

* [tls\_client\_server\_good.pcapng](https://gitlab.com/wireshark/wireshark/-/raw/master/samplecaptures/tls_client_server_good.pcapng)

**Задание:**

1. Настроить браузер с `SSLKEYLOGFILE`.
2. Захватить TLS-трафик, импортировать secrets в Wireshark.
3. Найти URI с аутентификацией или токеном.

---

## День 13. Анализ инцидента

**Пример pcap:**

### Пример PCAP

* **Архив:** [Wireshark‑tutorial‑identifying‑hosts‑and‑users‑5‑pcaps.zip](https://github.com/PaloAltoNetworks/Unit42-Wireshark-tutorials/raw/main/Wireshark-tutorial-identifying-hosts-and-users-5-pcaps.zip)
  *Размер: \~2 МБ*
  **Пароль для распаковки:** `infected`
* Извлеките любой файл из архива (например, `Wireshark-tutorial-identifying-hosts-and-users-5-pcaps-3.pcap`) и переименуйте его в `suspect.pcap` для удобства.

```bash
# 1. Запустите Zeek для разбора дампа
ezeek -r suspect.pcap

# 2. Проверяем, что создались базовые логи
tree -L 1  # увидите conn.log, http.log, dns.log, smtp.log, files.log и т.д.
```

*Основные логи, которые понадобятся:*

| Лог         | Назначение                             |
| ----------- | -------------------------------------- |
| `conn.log`  | Все сетевые подключения (5‑tuples)     |
| `http.log`  | HTTP‑запросы и ответы                  |
| `dns.log`   | DNS‑запросы и ответы                   |
| `smtp.log`  | SMTP‑сеансы, информация о письмах      |
| `files.log` | Метаданные извлечённых файлов (hashes) |

---

## Шаг 2. Построение `timeline.csv`

1. **Подготовьте syslog** (или сгенерируйте тестовый) в формате CSV:

   ```text
   2025-06-15T08:35:12Z,10.0.0.5,192.168.1.10,Failed SSH login
   2025-06-15T08:35:18Z,10.0.0.5,192.168.1.10,Account locked
   ```

2. **Склеиваем Zeek‑лог и syslog** c помощью Python (Pandas):

   ```python
   import pandas as pd

   # --- Zeek conn.log ---
   zeek = pd.read_table(
       'conn.log', comment='#', sep=r'\s+', engine='python',
       usecols=['ts', 'id.orig_h', 'id.resp_h', 'proto']
   ).rename(columns={
       'ts': 'epoch',
       'id.orig_h': 'src',
       'id.resp_h': 'dst',
       'proto': 'event'
   })
   zeek['ts'] = pd.to_datetime(zeek['epoch'], unit='s', utc=True)
   zeek = zeek[['ts', 'src', 'dst', 'event']]

   # --- Syslog (уже CSV) ---
   syslog = pd.read_csv('syslog.csv', names=['ts', 'src', 'dst', 'event'],
                        parse_dates=['ts'], utc=True)

   # --- Сводим и сортируем ---
   timeline = pd.concat([zeek, syslog]).sort_values('ts')
   timeline.to_csv('timeline.csv', index=False)
   print("timeline.csv готово")
   ```

*Файл `timeline.csv` будет иметь вид:*

```text
ts,src,dst,event
2025-06-15 08:35:12+00:00,10.0.0.5,192.168.1.10,Failed SSH login
2025-06-15 08:35:18+00:00,10.0.0.5,192.168.1.10,Account locked
...
```

---

## Шаг 3. Поиск индикаторов компрометации (IOC)

1. **DNS / HTTP**

   * Просмотрите `dns.log`, `http.log` на необычные домены, одноразовые TLD.
2. **Hash‑суммы файлов**

   * В `files.log` найдите `sha256`/`md5` скачанных объектов.
   * Проверяйте хэши на *VirusTotal*, *MalwareBazaar*, *Feodo Tracker* и др.
3. **SMTP‑трафик** (если есть)

   * Извлеките вложения, оцените тему/тело писем на фишинг.
4. **C2‑обращения**

   * В `conn.log` ищите частые небольшие сессии к одному IP, нетипичные порты.
5. **Отчёт**

   * Составьте список: `IOC, тип, описание (phishing site, loader, C2, etc.)`.

---

## День 14. Проектирование сети

**Задание:**

1. Нарисовать схему (draw\.io / diagrams.net)
2. VLSM-адресация + 3 ACL (SSH, HTTP, ICMP)

---

## День 15. Капстон

**Задание:**

1. Выбрать любую уязвимую VM (DVWA, Metasploitable).
2. Провести `nmap`, `bettercap`, `wireshark` анализ.
3. Подготовить отчёт + устную презентацию (5 мин).

---

> Убедитесь, что вы ежедневно сохраняете pcap, скрипты, выводы команд и делаете коммиты в Git-репозиторий!
