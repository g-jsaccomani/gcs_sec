# VPC Network Architecture Security Baseline

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))  
**Role:** Cloud Security Consultant  
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)  
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


Module responsible for VPC topology and flow logs, aligned with **CIS GCP Foundations Benchmark (Section 3)**.

## Networking Hardening Guidelines:
1. **Disable Default VPC:** Delete default networks and deploy custom VPC topologies with distinct subnets.
2. **VPC Flow Logs:** Enable flow logs with appropriate sampling rates on all production subnets.
