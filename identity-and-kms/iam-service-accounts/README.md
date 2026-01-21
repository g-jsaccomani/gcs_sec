# Service Accounts Hardening Baseline

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))  
**Role:** Cloud Security Consultant  
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)  
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


Module dedicated to securing project Service Accounts (SAs), aligned with **CIS GCP Foundations Benchmark (Section 1)**.

## Hardening Guidelines:
1. **Disable Static JSON Keys (CIS 1.4 / 1.5):** User-managed static private keys for Service Accounts are strictly forbidden. Adopt Workload Identity Federation or short-lived OIDC authentication.
2. **Least Privilege Binding:** Grant fine-grained, predefined or custom IAM roles instead of primitive `roles/editor` or `roles/owner`.

<!-- Checkpoint: 2026-01-21 - sec(exfiltration-prevention): apply VPC-SC perimeter policy on client analytical buckets -->
