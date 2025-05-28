# Теоретические материалы по информационной безопасности

> Эти материалы предназначены для самостоятельного изучения студентами колледжа перед выполнением тестов и практических заданий в рамках трёхнедельной практики по кибербезопасности.

---

## День 1. Основы ИБ и практика

### Роли в кибербезопасности

* **Blue Team** — защитники: мониторят, расследуют, устраняют угрозы.
* **Red Team** — атакующие: проводят тестирование на проникновение.
* **Purple Team** — объединяет red и blue для повышения эффективности.
* **GRC** — управление рисками, соблюдение стандартов и комплаенс.

### CIA-триада

* **Confidentiality (Конфиденциальность)** — защита от несанкционированного доступа.
* **Integrity (Целостность)** — защита от изменения данных.
* **Availability (Доступность)** — обеспечение доступности ресурсов.

### Cyber Kill Chain (Lockheed Martin)

1. Reconnaissance (разведка)
2. Weaponization (подготовка)
3. Delivery (доставка)
4. Exploitation (эксплуатация)
5. Installation (установка)
6. Command and Control (управление)
7. Actions on Objectives (достижение цели)

### Безопасная среда для лабораторий

* Используйте **изолированные виртуальные машины**.
* Делайте **снапшоты** перед каждой новой активностью.
* Обновляйте систему и инструменты.

---

## День 2. Сетевые основы

### Модель OSI и TCP/IP

| Уровень | OSI           | TCP/IP         |
| ------- | ------------- | -------------- |
| 7       | Приложений    | Application    |
| 6       | Представления | Application    |
| 5       | Сеансов       | Application    |
| 4       | Транспортный  | Transport      |
| 3       | Сетевой       | Internet       |
| 2       | Канальный     | Network Access |
| 1       | Физический    | Network Access |

### TCP-рукопожатие (Three-way handshake)

1. **SYN** → 2. **SYN/ACK** → 3. **ACK**

### Диапазоны портов

* **Well-known:** 0–1023 (HTTP: 80, HTTPS: 443, DNS: 53)
* **Registered:** 1024–49151
* **Dynamic/Private:** 49152–65535

### Wireshark — базовый фильтр

* `tcp`, `udp`, `icmp`, `http`, `ip.addr == x.x.x.x`

---

## День 3. Канальный уровень

### Ethernet-кадр

* Dst MAC | Src MAC | EtherType (0x0800 = IPv4) | Payload | CRC (FCS)

### ARP (Address Resolution Protocol)

* Используется для определения MAC по IP в локальной сети.
* Опкоды: 1 — Request, 2 — Reply

### ICMP (ping)

* **Echo Request (тип 8)** и **Echo Reply (тип 0)**
* TTL (Time To Live): предотвращает зацикливание пакетов

---

## День 4. IPv4 и Subnetting

### CIDR и маски

* CIDR-нотация: `/24` = 255.255.255.0
* Вычисление количества хостов: `2^(32 - префикс) - 2`

### VLSM (переменная длина маски)

* Используется для эффективного распределения адресов.

### Private IP диапазоны

* Class A: 10.0.0.0/8
* Class B: 172.16.0.0/12
* Class C: 192.168.0.0/16

---

## День 5. DHCP и NAT

### DHCP (Dynamic Host Configuration Protocol)

* Процесс DORA:

  1. **Discover**
  2. **Offer**
  3. **Request**
  4. **Ack**

### NAT и PAT

* **NAT (Network Address Translation):** замена IP-адреса
* **PAT (Port Address Translation):** NAT + замена порта (маскарадинг)

---

## День 6. Nmap и сканирование

### Типы сканов

* `-sS` — SYN-скан (stealth)
* `-sT` — TCP Connect
* `-sn` — Ping sweep (без портов)

### Состояния портов

* `open`, `closed`, `filtered`, `unfiltered`

---

## День 7. Nmap и NSE (скрипты)

### `-sV` — определение версий

### NSE (Nmap Scripting Engine)

* Категории: `default`, `safe`, `vuln`, `auth`, `brute`
* Запуск: `--script http-enum,vulners`

### CVSS

* Critical: 9–10
* High: 7–8.9
* Medium: 4–6.9
* Low: 0–3.9

---

## День 8. IDS и обход

### IDS (Snort, Suricata)

* Passive (p0f) vs Active OS-фингерпринтинг
* Обнаружение: `SYN+FIN`, unusual flags

### Evasion техники

* Подмена `--source-port 53`
* Увеличение `--data-length`
* Использование `--decoy`

---

## День 9. OpenVAS / GVM

### Компоненты

* Scanner
* Manager
* Web UI (GSAD)

### Authenticated vs Unauthenticated

* Повышенная точность при наличии учётных данных

---

## День 10. Sniffing / MITM

### Bettercap и ARP-spoof

* MITM в локальной сети: `arp.spoof on`
* Перехват трафика: `net.sniff on`

### SSL-Strip

* Удаляет HTTPS, превращая в HTTP (опасно)
* HSTS предотвращает это

---

## День 11. Wi-Fi безопасность

### WPA2-PSK

* 4-way handshake (EAPOL)
* PMKID — ключ аутентификации (можно захватить без клиента)

### Aircrack-ng

* Взлом PSK с использованием словаря (rockyou.txt)

---

## День 12. Web / TLS

### HTTP Headers

* Host, Cookie, User-Agent, Referer

### TLS 1.2

* ClientHello → ServerHello → Key Exchange → Change Cipher Spec → Encrypted handshake

### SNI

* Позволяет одному серверу обслуживать несколько доменов

---

## День 13. Инциденты и анализ

### CSIRT этапы

1. Detection
2. Triage
3. Containment
4. Eradication
5. Recovery
6. Lessons Learned

### IOC

* IP, хэш, домен, user-agent

### Zeek (ex-Bro)

* `conn.log`, `dns.log`, `http.log` — анализ сетевых событий

---

## День 14. Проектирование безопасной сети

### Зоны

* DMZ: полудоверенная зона (веб-серверы)
* Internal, Management, Guest Wi-Fi

### ACL

* `permit tcp host 192.168.1.10 any eq 22`

### Honeypots

* Low-interaction: эмуляция поверх TCP

---

## День 15. Повтор и OWASP Top 10

### OWASP TOP 10 (2021)

1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

---

> После изучения каждого раздела проверь себя с помощью тестов и переходи к практике. Удачи!
