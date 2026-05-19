# VPC Firewall Configuration Hardening Baseline

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))  
**Role:** Cloud Security Consultant  
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)  
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


Module responsible for management port security and network defense, aligned with **CIS GCP Foundations Benchmark (Section 3)**.

## Hardening Guidelines:
1. **Block Ingress SSH & RDP Globally (CIS 3.6 / 3.7):** Ingress rules allowing administrative ports (22, 3389) from `0.0.0.0/0` are strictly prohibited. Access must route through Identity-Aware Proxy (IAP) Bastion Hosts (CIDR: `35.235.240.0/20`).

<!-- Checkpoint: 2025-12-19 - sec(exfiltration-prevention): apply VPC-SC perimeter policy on client analytical buckets -->

<!-- Checkpoint: 2026-01-27 - sec(cmek-keys): add client CMEK key rotation verification and alerting automation -->

<!-- Checkpoint: 2026-02-19 - sec(lifecycle): automate lifecycle management rule audit for client compliance archive -->

<!-- Checkpoint: 2026-05-19 - sec(exfiltration-prevention): apply VPC-SC perimeter policy on client analytical buckets -->
