# Cloud Logging & Monitoring Security Baseline

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))  
**Role:** Cloud Security Consultant  
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)  
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


Module responsible for central audit telemetry and threat detection, aligned with **CIS GCP Foundations Benchmark (Section 2)**.

## Audit Logging Guidelines:
1. **Data Access Audit Logs:** Enable Data Read, Data Write, and Admin Activity logs across all core GCP services.
2. **Log Router Sinks:** Stream centralized audit logs into BigQuery and Google SecOps.

<!-- Checkpoint: 2026-01-29 - sec(exfiltration-prevention): apply VPC-SC perimeter policy on client analytical buckets -->

<!-- Checkpoint: 2026-03-26 - sec(cmek-keys): add client CMEK key rotation verification and alerting automation -->

<!-- Checkpoint: 2026-04-09 - docs(runbook): add client incident response playbook for public bucket alerts -->

<!-- Checkpoint: 2026-05-01 - sec(exfiltration-prevention): apply VPC-SC perimeter policy on client analytical buckets -->

<!-- Checkpoint: 2026-07-13 - sec(lifecycle): automate lifecycle management rule audit for client compliance archive -->
