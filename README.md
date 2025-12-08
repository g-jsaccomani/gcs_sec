# Google Cloud Security (GCS) Hardening Framework
## Automated CIS Benchmark Auditing, Remediation & Governance

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))
**Role:** Cloud Security Consultant
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


A comprehensive framework for automated auditing, configuration assessment, and proactive remediation of Google Cloud environments aligned with the **CIS Google Cloud Foundations Benchmark**.

---

## Key Focus Areas

1. **Identity & Access Management (IAM)**: Service Account key retirement, Workload Identity, and least privilege.
2. **Networking & Firewalls**: Elimination of open ingress ports (22, 3389), IAP bastion configuration, and flow logging.
3. **Data Protection & Storage**: Uniform Bucket-Level Access, Public Access Prevention, CMEK, and Cloud SQL SSL.
4. **Compute & Workloads**: Shielded VMs, OS Login, and Private GKE architectures.
5. **Auditing & SIEM**: Cloud Audit Logging and centralized SecOps streaming.

---

## Repository Structure

```text
gcs_sec/
 compute/
    gce-instances/                        # Compute Engine hardening & audit scripts
    gke-clusters/                         # GKE cluster security configs
 identity-and-kms/
    iam-service-accounts/                 # Service account governance
    kms-keys/                             # KMS key rotation & CMEK policies
 logging-and-monitoring/
    audit-logs/                           # Audit logging configs & sinks
 networking/
    vpc-firewall/                         # Firewall rules & IAP ingress controls
    vpc-networks/                         # VPC topologies & flow log configs
 storage-and-data/
    cloud-sql/                            # Cloud SQL SSL & private IP configs
    gcs-buckets/                          # GCS UBLA & PAP policies
 docs/                                     # Architecture & CIS baseline docs
 orchestrate_gcp_hardening_environments.py # Central auditing & remediation orchestrator
 .gitignore
 CODE_OF_CONDUCT.md
 LICENSE
 README.md
 SECURITY.md
```

---

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))
**Role:** Cloud Security Consultant
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


<!-- Checkpoint: 2025-12-08 - sec(cmek-keys): add client CMEK key rotation verification and alerting automation -->
