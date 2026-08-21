# Cloud SQL Database Security Baseline

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))  
**Role:** Cloud Security Consultant  
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)  
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


Module responsible for hardening relational database instances (PostgreSQL, MySQL, SQL Server), aligned with **CIS GCP Foundations Benchmark (Section 6)**.

## Database Hardening Guidelines:
1. **Private IP Only (CIS 6.5 / 6.6):** Disable public IP whitelists (`0.0.0.0/0`). Database traffic must route strictly via Private Service Connect or Private Services Access in VPC subnets.
2. **Enforce Encryption in Transit (CIS 6.4):** Enforce SSL/TLS certificates for all client connections.
3. **Automated Daily Backups (CIS 6.7):** Maintain automated, versioned daily backups with point-in-time recovery.
