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

* [2024-09-04-traffic-analysis-exercise.pcap](https://www.malware-traffic-analysis.net/2024/09/04/2024-09-04-traffic-analysis-exercise.pcap.zip) (пароль: `infected`)

**Задание:**

1. `zeek -r suspect.pcap`
2. Объединить с syslog, построить timeline.csv (ts, src, dst, event).
3. Найти IOC.

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
