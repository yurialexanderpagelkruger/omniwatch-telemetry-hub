# OmniWatch

**OmniWatch** is a centralized telemetry, proactive monitoring, and multi-site alerting platform engineered for organizations with distributed branch offices or multi-server infrastructure. Specifically designed for IT consultants, system administrators, and operations leads in SMBs, *OmniWatch* replaces the reactive break-fix model with comprehensive real-time visibility across computing resources, network connectivity, and service availability.

Featuring lightweight collection agents for remote hosts, an interactive dashboard for immediate visual tracking, and a multi-channel notification engine (Telegram and Email), the platform identifies bottlenecks and incidents before they disrupt operations or customer service, while also including an interactive demo mode for live client presentations.

---

### 📸 Screenshots

<div align="center">
  <table border="0">
    <thead>
      <tr>
        <th align="center">Desktop Version</th>
        <th align="center">Mobile Version</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td align="center" valign="middle">
          <img src="screenshot.gif" alt="Desktop Version" width="589" />
        </td>
        <td align="center" valign="middle">
          <img src="screenshot2.gif" alt="Mobile Version" width="186" />
        </td>
      </tr>
    </tbody>
  </table>
</div>

---

## ✨ Key Features

* **Unified Multi-Site Topology:** Centralized grouping of geographically distributed branches with live health-status visualization (Online, Warning, Critical).

* **Multi-Language Support (i18n):** Fully localized web interface offering support for 3 languages: English, Spanish, and Portuguese, ensuring seamless operation for multilingual teams.

* **Adaptive Theming (Dark & Light Mode):** Dynamic UI theme switching between Dark and Light mode, optimized for prolonged monitoring sessions in Network Operations Centers (NOC) and high-ambient light environments.

* **Ultra-Lightweight Collector Agent:** Dependency-free Bash script extracting CPU load, memory utilization, disk saturation, network latency, and critical service integrity (`systemd`), reporting back through a secure REST API.

* **Automated Real-Time Alerts:** Proactive delivery of critical incident alerts to Telegram groups or email inboxes triggered by service outages, node disconnections, or resource exhaustion.

* **Demo Mode with Dynamic Simulation:** Seamless toggle between live production telemetry and synthetic real-time metrics for portfolio showcases and client walkthroughs without exposing production nodes.

* **Core Performance Metrics:** Real-time logging and visual representation of RAM usage, root partition storage saturation, average CPU load, and essential service inspection (Web servers, Databases, ERPs).

* **Responsive Real-Time Web Dashboard:** Frontend built with Python/Flask and Vanilla JavaScript featuring periodic asynchronous updates without full-page reloads.

---

## ⚙️ What It Does (Available Modules)

From edge host monitoring to centralized operational dispatch, *OmniWatch* includes the following core components:

1. **Central Server & API Hub (`app.py`):** Exposes token-authenticated endpoints for telemetry ingestion (`/api/report`), evaluates alert thresholds, and delivers consolidated data to the web dashboard.

2. **Server Collection Agent (`agent/collector_agent.sh`):** Executes scheduled tasks across host sites, queries operating system performance metrics, and reliably dispatches payload data to the central Hub.

3. **Internationalization & Theming Layer:** Client-side localization and styling controller managing 3 language dictionaries (English, Spanish, Portuguese) alongside smooth Dark/Light mode theme state persistence.

4. **Visual Monitoring Dashboard (`templates/index.html`, `dashboard.js`):** Responsive web interface that automatically refreshes operational indicators every 5 seconds through asynchronous REST API calls.

5. **Alert Notification Engine:** Continuously tracks critical thresholds (>90% disk usage, >90% RAM utilization, or node dropouts) and routes formatted alerts to technical on-call channels.

6. **Telemetry Simulator:** Synthesizes realistic traffic variance and system load oscillations for live demonstrations and testing environments.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.10+ / Flask.
* **Frontend:** Semantic HTML5, Vanilla CSS3 (custom CSS variables supporting Dark and Light modes), and asynchronous JavaScript (Fetch API).
* **Internationalization:** Client-side i18n dictionary mapping (English, Spanish, Portuguese).
* **Collection Agents:** POSIX-compliant Bash, GNU Coreutils, `curl`, `awk`.
* **Third-Party Integraciones:** Telegram Bot API, SMTP/Email.
* **Security & Networking:** Bearer token authentication on REST APIs with production support for VPN and HTTPS deployment.

---

## 🚀 Installation and Usage

1. Clone the repository on the central monitoring server:
   ```bash
   git clone [https://github.com/yurialexanderpagelkruger/omniwatch-telemetry-hub.git](https://github.com/yurialexanderpagelkruger/omniwatch-telemetry-hub.git)
   cd omniwatch-telemetry-hub

## 👨‍💻 Author

Developed by **Yuri Alexander Pagel Krüger**
