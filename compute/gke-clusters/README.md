# GKE Cluster Security Hardening Baseline

---
**Author:** Joabson Saccomani ([@jsaccomani](https://github.com/g-jsaccomani))  
**Role:** Cloud Security Consultant  
**LinkedIn:** [linkedin.com/in/jsaccomani](https://www.linkedin.com/in/jsaccomani)  
*Copyright © 2026 Google LLC / Joabson Saccomani. All rights reserved. Distributed under the Apache License 2.0.*


Module responsible for foundational Kubernetes security, aligned with **CIS GCP Foundations Benchmark (Section 4)** and **CIS GKE Benchmark**.

## Cluster Hardening Guidelines:
1. **Private GKE Clusters:** Enforce private nodes and restricted control plane authorized networks.
2. **Workload Identity:** Enable GKE Workload Identity on all node pools.
3. **Dataplane V2:** Enable Cilium-powered eBPF Dataplane V2 for network isolation and monitoring.

<!-- Checkpoint: 2025-12-22 - sec(lifecycle): automate lifecycle management rule audit for client compliance archive -->

<!-- Checkpoint: 2026-02-06 - sec(exfiltration-prevention): apply VPC-SC perimeter policy on client analytical buckets -->

<!-- Checkpoint: 2026-02-09 - sec(lifecycle): automate lifecycle management rule audit for client compliance archive -->

<!-- Checkpoint: 2026-03-06 - sec(cmek-keys): add client CMEK key rotation verification and alerting automation -->

<!-- Checkpoint: 2026-03-18 - sec(cmek-keys): add client CMEK key rotation verification and alerting automation -->

<!-- Checkpoint: 2026-03-24 - sec(lifecycle): automate lifecycle management rule audit for client compliance archive -->

<!-- Checkpoint: 2026-06-16 - docs(runbook): add client incident response playbook for public bucket alerts -->
