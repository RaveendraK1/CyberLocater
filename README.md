# 🌍 CyberLocator v2.0 - Advanced OSINT & IP Threat Intelligence Platform

![CyberLocator Banner](https://img.shields.io/badge/Cyber-Intelligence-00ffaa?style=for-the-badge&logo=hackthebox)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![JavaScript](https://img.shields.io/badge/Vanilla-JS-yellow?style=for-the-badge&logo=javascript)

**CyberLocator** is a powerful, lightweight, and incredibly fast OSINT (Open-Source Intelligence) web dashboard designed for cyber-security investigators, ethical hackers, and law enforcement. It allows investigators to deeply analyze suspicious IP addresses by detecting VPN/Proxies, pulling raw WHOIS registration data, tracking live network traceroutes, and cross-referencing global cybercrime blacklists.

---

## 🚀 Key Features

*   **📍 Advanced IP Geolocation**: Get precise coordinates, City, Region, ZIP, Timezone, and ISP details instantly, plotted on an interactive cyber-themed tactical map (powered by Leaflet.js).
*   **🛡️ VPN & Datacenter Unmasking**: Uses AI heuristics and metadata flags to determine if an IP is hiding behind a commercial VPN, Tor node, or Cloud Datacenter (e.g., AWS, Linode).
*   **🕵️ Native WHOIS Lookup Engine**: Bypasses rate-limited APIs by using a custom Python socket client that queries the root `whois.iana.org` server directly to fetch raw owner registration data and abuse contact emails.
*   **🛣️ Custom Network Path Analyzer (MTR)**: Runs a highly optimized (500ms timeout per hop) native Windows `tracert` from the backend to identify upstream ISPs and network gateways.
*   **🚨 Threat Intel & OSINT Deep Links**: Generates instant heuristics on Abuse scores and provides 1-click deep links to search the suspect IP on **VirusTotal**, **AbuseIPDB**, and **Scamalytics**.
*   **🎨 Premium Glassmorphism UI**: A stunning, animated, dark "cyber-hacker" visual theme built entirely with Vanilla CSS—no heavy frameworks required.

---

## 🛠️ Tech Stack

*   **Frontend**: HTML5, CSS3 (Glassmorphism UI), Vanilla JavaScript.
*   **Backend**: Python 3.x (`http.server`, `socket`, `subprocess`).
*   **Libraries / APIs**: Leaflet.js (Tactical Map), IP-API (Geolocation & Network Identity).

---

## 💻 Installation & Usage

CyberLocator is designed to be plug-and-play. No complex databases or `npm install` required!

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/CyberLocator.git
    cd CyberLocator
    ```

2.  **Start the Local Backend Server**:
    Run the provided Python script to spin up the API and Web Server.
    ```bash
    python run.py
    ```

3.  **Launch Dashboard**:
    The script will automatically open your default web browser to `http://localhost:8000`. Simply enter a suspicious IP address and hit "Trace Location"!

---

## 🔍 How the "AI Analyst Note" Works

When you scan an IP, CyberLocator doesn't just show data; it provides an automated investigation strategy. 
*   If a **Residential IP** is detected, it confirms the physical location is highly likely to be accurate.
*   If a **Datacenter/VPN** is detected, it flags the IP as *Masked* and advises the investigator to send a Lawful Interception Subpoena to the owning ISP/ASN (which can be easily found in the adjacent WHOIS panel).

---

## ⚠️ Disclaimer

*This tool is intended for legal and authorized use by cyber security researchers, SOC analysts, and law enforcement agencies. Do not use this tool for malicious purposes. The developer assumes no liability for the misuse of the data provided.*

---
**Maintained with ❤️ by [Your Name/Handle]**
