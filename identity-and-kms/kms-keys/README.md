# Cloud KMS Key Management Security Baseline

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))  
**Role:** Cloud Security Consultant  
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)  
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


Module responsible for cryptographic key governance, aligned with **CIS GCP Foundations Benchmark (Section 1)**.

## KMS Hardening Guidelines:
1. **Automated Key Rotation (CIS 1.9):** Enforce automatic rotation schedules of 90 days or less on all cryptographic keys.
2. **Separation of Duties:** Restrict `roles/cloudkms.cryptoKeyDecrypter` and `roles/cloudkms.admin` to distinct service principles.

<!-- Checkpoint: 2026-01-05 - sec(lifecycle): automate lifecycle management rule audit for client compliance archive -->

<!-- Checkpoint: 2026-02-24 - sec(exfiltration-prevention): apply VPC-SC perimeter policy on client analytical buckets -->

<!-- Checkpoint: 2026-03-20 - sec(exfiltration-prevention): apply VPC-SC perimeter policy on client analytical buckets -->

<!-- Checkpoint: 2026-04-07 - sec(cmek-keys): add client CMEK key rotation verification and alerting automation -->
