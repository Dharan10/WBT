# WBT - Advanced Enhancement Roadmap

This document outlines the strategic roadmap to transform WBT into an industry-leading WAF testing platform.

## 1. 🧠 Smart Evasion & Obfuscation (The "Brain")
**Goal**: Test WAF robustness against advanced evasion techniques, not just static signatures.
- [ ] **Core**: Implement a `MutationEngine` in Python to apply transformations.
- [ ] **Technique 1**: URL Encoding (`<` -> `%3C`, double encoding `%253C`).
- [ ] **Technique 2**: Case Switching (`SELECT` -> `SeLeCt`).
- [ ] **Technique 3**: Whitespace Manipulation (SQLi: `UNION SELECT` -> `UNION/**/SELECT`).
- [ ] **UI**: Add "Evasion Level" slider (None -> Low -> High) in Configuration.

## 2. 🔌 Cloud WAF Integrations
**Goal**: Support verifying blocks on major cloud providers where we don't have direct access to log files.
- [ ] **Architecture**: Refactor `BaseWAFAdapter` to support async API polling.
- [ ] **AWS WAF**: Implement adapter using `boto3` to query CloudWatch Logs / GetSampledRequests.
- [ ] **Cloudflare**: Implement adapter using Cloudflare GraphQL Analytics API.
- [ ] **UI**: Add dropdown to select Adapter Type (Local File vs. API) and input fields for API Keys/Secrets.

## 3. 🔄 CI/CD Automation (Headless Mode)
**Goal**: Enable WBT to run in GitHub Actions/GitLab CI pipelines to fail builds on security regression.
- [ ] **CLI**: Create `cli.py` entrypoint using `argparse` or `typer`.
    - `python wbt-cli.py --target http://staging --config wbt.yaml --fail-under 90`
- [ ] **Exit Codes**: Ensure proper exit codes (0 = Pass, 1 = Fail score, 2 = Error).
- [ ] **Output**: Generate JUnit XML report for CI/CD visualization.

## 4. 🚦 HAR Replay (Realistic Traffic)
**Goal**: Test WAFs against stateful, authenticated, real-world user workflows.
- [ ] **Backend**: Add `.har` file parser (using `haralyzer` or generic JSON).
- [ ] **Engine**: Create `ReplayTrafficGenerator` that extracts method, URL, headers, and body from HAR entries.
- [ ] **UI**: Add File Upload zone in Config -> "Traffic Source" to upload a user session.
- [ ] **Feature**: "Mix Mode" -> Insert attack payloads *into* the HAR request parameters dynamically.

## 5. 📉 Compliance & Comparative Reporting
**Goal**: Speak "Management Language" (PCI, SOC2) and allow A/B testing of WAF vendors.
- [ ] **Tagging**: Update `payloads.yaml` schema to include tags: `ip_reputation`, `pci_dss`, `owasp_top_10`.
- [ ] **Reporting**: Update `ReportGenerator` to group failures by these tags.
    - *Example*: "You failed 3 checks required for PCI-DSS Compliance."
- [ ] **Comparison**: (Future) Ability to select two report JSONs and generate a "Diff".
