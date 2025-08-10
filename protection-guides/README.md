# CISO Project — Offensive & Defensive Security for Active Directory (Updated 2025)

![AD Attack–Defense Map](scheme/ad_attack_defense_map.png)
[Источник схемы (.drawio)](scheme/ad_attack_defense_map.drawio)

## 📂 Sections

### 1. Attacks
- NTLM Relay
- Kerberos Attacks
- DHCP Spoofing
- Zerologon
- PrinterBug
- MSSQL Relay / HTTP Relay
- BadSuccessor (dMSA Abuse)
- Golden dMSA Attack
- AD Trusts Attack Paths
- Hybrid AD Authentication Bypass
- LLMNR Poisoning (Updated)
- SMB Relay (Updated)
- IPv6 Relay (MITM6)
- Pass-the-Hash
- Kerberoasting (Updated)

### 2. Tools
- Responder — LLMNR/NBT-NS poisoning
- Impacket — SMB/LDAP/HTTP relays
- psexec — Remote code execution via SMB
- mitm6 — IPv6-based MITM
- CrackMapExec — SMB/WinRM/RDP automation
- BloodHound — AD privilege graph
- Mimikatz / pypykatz — Credential dumping
- SharpHound — Data collection for BloodHound

### 3. Protection
- [Hardening Active Directory](protection/hardening-active-directory.md)
- [Hardening SMB/LDAP](protection/hardening-smb-ldap.md)
- [Hardening DHCP/DNS](protection/hardening-dhcp-dns.md)
- [Hardening Endpoints](protection/hardening-endpoints.md)
- [Network Segmentation](protection/network-segmentation.md)

### 4. SIEM
- [SIEM Monitoring Recommendations (2025)](SIEM_monitoring_recommendations.md)

### 5. Playbooks (2025)
- [Playbook — NTLM Relay](playbooks/playbook-ntlm-relay.md)
- [Playbook — AD dMSA Compromise (BadSuccessor + Golden dMSA)](playbooks/playbook-ad-dmsa-compromise.md)
- [Playbook — Kerberoasting (gMSA Focus)](playbooks/playbook-kerberoasting-gmsa.md)
- [Playbook — Hybrid AD Authentication Bypass](playbooks/playbook-hybrid-ad-bypass.md)
- [Playbook — AD Trusts Attack Paths Abuse](playbooks/playbook-ad-trusts-abuse.md)

---

## 📌 Notes
- All attack and defense content is for **lab and educational use only**.
- Each section links directly to detailed `.md` guides.
- MITRE ATT&CK mappings are included for SOC correlation.

