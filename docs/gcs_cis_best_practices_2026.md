# Google Cloud Storage (GCS) Hardening & CIS Best Practices (2026 Baseline)

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))
**Role:** Cloud Security Consultant
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


This document outlines consolidated best practices (CIS Google Cloud Foundation Benchmark, Google Cloud Architecture Framework, and industry standards) for data protection, compliance, and governance in Google Cloud Storage.

---

## 1. Identity & Access Management (IAM)

- **Uniform Bucket-Level Access (UBLA)**:
  - Enforce `Uniform Bucket-Level Access` on all buckets to disable legacy ACLs and unify access control strictly within IAM.
  - *Policy*: `constraints/storage.uniformBucketLevelAccess` enforced at Organization or Folder level.
- **Public Access Prevention (PAP)**:
  - Enforce `enforcePublicAccessPrevention = true` on buckets storing internal or confidential data.
  - *Org Policy*: `constraints/storage.publicAccessPrevention` set to `ENFORCE`.
- **Principle of Least Privilege & Workload Identity**:
  - Avoid primitive roles (`Owner`, `Editor`).
  - Use **Workload Identity Federation** for workloads accessing GCS from external environments or Kubernetes without static service account keys.

---

## 2. Data Protection & Cryptography

- **Customer-Managed Encryption Keys (CMEK with Cloud KMS)**:
  - Buckets containing Sensitive Data or PII must use customer-managed encryption keys (CMEK) with automated key rotation (maximum 90 days).
- **Soft Delete and Object Retention Lock**:
  - Enable **Soft Delete** (default retention 7 to 30 days) to prevent ransomware attacks and accidental deletion.
  - For regulatory compliance (WORM - Write Once, Read Many), configure **Object Retention Lock** and **Bucket Lock**.
- **Sensitive Data Protection Integration**:
  - Automate discovery and classification scans for sensitive data (PII, financial data, credentials) at rest in GCS.

---

## 3. Network Security & Perimeter Isolation

- **VPC Service Controls (VPC-SC)**:
  - Restrict storage API access to authorized service perimeters, mitigating data exfiltration risks.
- **Private Google Access / Private Service Connect (PSC)**:
  - All internal traffic from VPC subnets must route privately without traversal over the public internet.

---

## 4. Auditing, Telemetry & Monitoring

- **Cloud Audit Logs (Data Access Logs)**:
  - Enable **Admin Activity** and **Data Access Logs** (Read/Write) for `storage.googleapis.com`.
- **Telemetry Export to Google SecOps (SIEM)**:
  - Route audit logs from critical buckets to Google SecOps for real-time anomaly detection.

---

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))
**Role:** Cloud Security Consultant
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


<!-- Checkpoint: 2025-12-09 - docs(runbook): add client incident response playbook for public bucket alerts -->
