# Compute Engine (GCE) Instance Hardening Baseline

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))  
**Role:** Cloud Security Consultant  
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)  
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


Module responsible for securing virtual machine instances, aligned with **CIS GCP Foundations Benchmark (Section 4)**.

## Compute Hardening Guidelines:
1. **Shielded VM Enforcement:** Enable Secure Boot, vTPM, and Integrity Monitoring on all Compute Engine instances.
2. **OS Login Enforcement:** Manage SSH keys centrally via Google Cloud IAM OS Login.
3. **Restrict Public IPs:** VM instances must reside on private subnets with Cloud NAT for outbound internet access.

<!-- Checkpoint: 2026-01-30 - docs(runbook): add client incident response playbook for public bucket alerts -->

<!-- Checkpoint: 2026-02-13 - sec(cmek-keys): add client CMEK key rotation verification and alerting automation -->

<!-- Checkpoint: 2026-04-13 - sec(cmek-keys): add client CMEK key rotation verification and alerting automation -->

<!-- Checkpoint: 2026-05-04 - docs(runbook): add client incident response playbook for public bucket alerts -->

<!-- Checkpoint: 2026-05-07 - sec(cmek-keys): add client CMEK key rotation verification and alerting automation -->

<!-- Checkpoint: 2026-06-03 - docs(runbook): add client incident response playbook for public bucket alerts -->
