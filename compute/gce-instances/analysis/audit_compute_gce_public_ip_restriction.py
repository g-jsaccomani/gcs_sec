# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: audit_compute_gce_public_ip_restriction.py
Control: CIS GCP v4.0.0 - Controle 4.9 (Ensure GCE instances do not have external IP addresses)
Description: Ensures complete network edge isolation by validating if any VM has an external public IP.
Required IAM: roles/compute.viewer
"""
import sys
import json
import logging
# pyrefly: ignore [missing-import]
from google.cloud import compute_v1
# pyrefly: ignore [missing-import]
from google.auth import default

# [CCSE_CONFIG_INJECTION_START]
# Configuration placeholder. Injected dynamically by master orchestrator.
INJECTED_ENV_CONFIG = {}
# [CCSE_CONFIG_INJECTION_END]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

def audit_public_ips():
    report = {
        "audit_metadata": {
            "control_id": "CIS_GCP_4.0.0_4.9",
            "control_name": "GCE Public IP Network Isolation",
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

        client = compute_v1.InstancesClient(credentials=credentials)
        request = compute_v1.AggregatedListInstancesRequest(project=project_id)
        instances_iterator = client.aggregated_list(request=request)
        
        total_vms = 0
        failed_vms = 0

        for zone, response in instances_iterator:
            if response.instances:
                for instance in response.instances:
                    total_vms += 1
                    has_public_ip = False
                    
                    if instance.network_interfaces:
                        for ni in instance.network_interfaces:
                            if ni.access_configs:
                                # Presence of access_config indicates associated External IP
                                for ac in ni.access_configs:
                                    if ac.nat_i_p:
                                        has_public_ip = True

                    if has_public_ip:
                        failed_vms += 1
                        report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
                        report["audit_findings"].append({
                            "control_category": "NETWORK_PERIMETER_SSRF",
                            "standard_reference": "CIS GCP 4.9",
                            "control_id": "CIS_GCP_4.9",
                            "control_name": "No GCE External Public IPs",
                            "evaluation_status": "FAILED",
                            "severity_level": "HIGH",
                            "resource_affected": instance.name,
                            "finding_details": f"Instance {instance.name} is directly exposed with an external IP address.",
                            "remediation_instructions": "Remove the access_config {} section from the VM's network interface block and configure Cloud NAT."
                        })

        report["compliance_summary"]["total_checks_executed"] = total_vms
        report["compliance_summary"]["failed_checks"] = failed_vms
        report["compliance_summary"]["passed_checks"] = total_vms - failed_vms
        if total_vms > 0:
            report["compliance_summary"]["compliance_score"] = ((total_vms - failed_vms) / total_vms) * 100.0

        print(json.dumps(report, indent=2))
        sys.exit(1 if failed_vms > 0 else 0)

    except Exception as e:
        logging.error(f"Error executing audit: {str(e)}")
        print(json.dumps({"status": "ERROR", "message": str(e)}, indent=2))
        sys.exit(2)

if __name__ == "__main__":
    audit_public_ips()

# Audit checkpoint [2025-12-17]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2025-12-22]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2025-12-23]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone

# Audit checkpoint [2026-01-03]: feat(audit-logging): configure Cloud Audit Logs streaming to client Splunk SIEM

# Audit checkpoint [2026-02-06]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads
