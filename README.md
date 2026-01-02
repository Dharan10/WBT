# WBT - WAF Benchmark Toolkit

**WAF Benchmark Toolkit (WBT)** is an open-source, industry-grade platform for evaluating the effectiveness of Web Application Firewalls (WAFs). It provides a reproducible feedback loop of attacks, traffic simulation, analysis, and scoring.

![WBT Dashboard](https://via.placeholder.com/800x400?text=WBT+Dashboard+Preview)

## 🚀 Key Features

*   **Automated Benchmarking**: One-click execution of thousands of attack vectors.
*   **Dual-Traffc Engines**: Simulates both *legitimate* user behavior and *malicious* attacks concurrently.
*   **Detailed Reporting**: Generates immediate JSON/PDF reports with bypass analysis.
*   **Pluggable Architecture**: Easily add new WAF adapters, custom attack payloads, or target configurations.
*   **Real-time Analytics**: Live dashboard showing traffic throughput, block rates, and system logs.

---

## 🛠️ Configuration Guide

### 1. Defining a Target
Targets are defined in `configs/target.yaml`. You can modify this file directly or use the **Config** page in the web UI.

```yaml
target:
  url: "http://waf_target:8080"  # The entry point of your WAF
  timeout: 10                     # Request timeout in seconds
  concurrency: 5                  # Number of concurrent users/attackers
  headers:                        # Custom headers (e.g., for Auth)
    Authorization: "Bearer token"
    X-Custom-Auth: "secret"
```

### 2. Custom Attack Payloads
WBT loads attack definitions from the `payloads/` directory. You can add your own `.yaml` files here.

**Structure of a Payload File:**
```yaml
category: "SQL Injection"
vectors:
  - id: "sqli-custom-001"
    payload: "' OR '1'='1"
    method: "POST"          # GET, POST, PUT, DELETE
    location: "body"        # 'query', 'body', 'header', 'path'
```
*   **category**: Grouping for reports.
*   **payload**: The malicious string to inject.
*   **location**: Where to inject (`query` = `?q=payload`, `body` = JSON/Form data).

---

## 🔌 Adapters & Extensibility

WBT uses a modular adapter system to interface with different WAFs.

### Supported Adapters
*   **ModSecurity (Nginx)**: Built-in default. Reads `modsec_audit.log`.

### Implementing a Custom Adapter
To support a new WAF (e.g., AWS WAF, Cloudflare, Azure), you need to create a new Python class inheriting from `BaseWAFAdapter`.

**1. Create file `waf_adapters/my_custom_waf.py`:**
```python
from .base import BaseWAFAdapter
from typing import List, Dict

class CustomWAFAdapter(BaseWAFAdapter):
    def fetch_logs(self, start_time: float) -> List[Dict]:
        # Implement API call to your WAF provider
        # Return list of log entries
        return []
```

**2. Register the Adapter:**
Update `waf_adapters/__init__.py` to include your new class in the factory method.

---

## 📊 Understanding Reports

Reports are generated in `reports/`.

*   **Score**: A 0-100 rating based on the percentage of blocked attacks vs. false positives.
*   **Blocked Attacks**: Attacks that received a 403/406/500 response.
*   **Bypasses (False Negatives)**: Attacks that received a 200 OK. **These are critical findings.**
*   **False Positives**: Legitimate traffic that was incorrectly blocked.

**View Reports:**
Navigate to the **Reports** tab in the UI to preview JSON data or download PDF summaries.

---

## ⚡ Quick Start

1.  **Start the Stack**:
    ```bash
    docker-compose up -d --build
    ```
2.  **Access UI**:
    Open [http://localhost:3000](http://localhost:3000)
3.  **Run Benchmark**:
    Go to Dashboard -> Click "Start Benchmark".

---

## 🤝 Contributing

Contributions are welcome! Please submit a Pull Request with your new adapters or payloads.
