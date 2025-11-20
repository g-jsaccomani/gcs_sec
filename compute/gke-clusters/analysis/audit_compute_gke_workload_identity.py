# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: audit_compute_gke_workload_identity.py
Control: CIS GKE Benchmark - Controle 5.2 (Ensure GKE Workload Identity is Enabled)
Description: Strictly Read-Only Audit que valida se o cluster Kubernetes está rodando com Workload Identity ativo.
Required IAM: roles/container.viewer
"""
import sys
import json
import logging
# pyrefly: ignore [missing-import]
from google.cloud import container_v1
# pyrefly: ignore [missing-import]
from google.auth import default

# [CCSE_CONFIG_INJECTION_START]
# Configuration placeholder. Injected dynamically by master orchestrator.
INJECTED_ENV_CONFIG = {}
# [CCSE_CONFIG_INJECTION_END]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

def audit_gke_wi():
    report = {
        "audit_metadata": {
            "control_id": "CIS_GKE_5.2",
            "control_name": "GKE Workload Identity Check",
            "compliance_agent_version": "2.4.0",
        },
        "compliance_summary": {
            "overall_status": "COMPLIANT",
            "compliance_score": 100.0,
            "total_checks_executed": 0,
            "passed_checks": 0,
            "failed_checks": 0
        },
        "audit_findings": []
    }

    try:
        credentials, project_id = default()
        if not project_id:
            print(json.dumps({"status": "ERROR", "message": "Failed to resolve GCP Project ID"}, indent=2))
            sys.exit(2)

        client = container_v1.ClusterManagerClient(credentials=credentials)
        response = client.list_clusters(project_id=project_id, zone="-")
        
        clusters = response.clusters
        report["compliance_summary"]["total_checks_executed"] = len(clusters)
        
        if len(clusters) == 0:
            print(json.dumps(report, indent=2))
            sys.exit(0)

        failed_count = 0
        for cluster in clusters:
            wi_enabled = False
            if cluster.workload_identity_config and cluster.workload_identity_config.workload_pool:
                wi_enabled = True

            if not wi_enabled:
                failed_count += 1
                report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
                report["audit_findings"].append({
                    "control_category": "IDENTITY_AUTH_IAM",
                    "standard_reference": "CIS GKE 5.2",
                    "control_id": "CIS_GKE_5.2",
                    "control_name": "Enforce GKE Workload Identity",
                    "evaluation_status": "FAILED",
                    "severity_level": "CRITICAL",
                    "resource_affected": cluster.name,
                    "finding_details": f"Cluster {cluster.name} does not have Workload Identity configured. Workloads may fall back to default metadata service accounts.",
                    "remediation_instructions": "Configure the workload_identity_config block in Terraform and associate the ServiceAccounts."
                })

        report["compliance_summary"]["failed_checks"] = failed_count
        report["compliance_summary"]["passed_checks"] = len(clusters) - failed_count
        report["compliance_summary"]["compliance_score"] = ((len(clusters) - failed_count) / len(clusters)) * 100.0

        print(json.dumps(report, indent=2))
        sys.exit(1 if failed_count > 0 else 0)

    except Exception as e:
        logging.error(f"Error executing audit: {str(e)}")
        print(json.dumps({"status": "ERROR", "message": str(e)}, indent=2))
        sys.exit(2)

if __name__ == "__main__":
    audit_gke_wi()
