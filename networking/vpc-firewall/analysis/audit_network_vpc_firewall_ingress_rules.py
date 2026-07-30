# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: audit_network_vpc_firewall_ingress_rules.py
Control: CIS GCP v4.0.0 - Controle 3.6 / 3.7 (Ensure no firewall rules allow SSH/RDP from 0.0.0.0/0)
Description: Strictly Read-Only Audit que verifica se alguma regra de firewall permite acesso direto a portas 22/3389 de qualquer IP.
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

def audit_firewall_rules():
    report = {
        "audit_metadata": {
            "control_id": "CIS_GCP_4.0.0_3.6",
            "control_name": "Firewall Public Management Ports Validation",
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

        client = compute_v1.FirewallsClient(credentials=credentials)
        firewalls = list(client.list(project=project_id))
        
        report["compliance_summary"]["total_checks_executed"] = len(firewalls)
        if len(firewalls) == 0:
            print(json.dumps(report, indent=2))
            sys.exit(0)

        failed_count = 0
        for fw in firewalls:
            if fw.direction == "INGRESS" and "0.0.0.0/0" in fw.source_ranges:
                is_unsafe = False
                for allowed in fw.allowed:
                    if allowed.i_p_protocol == "all":
                        is_unsafe = True
                    elif allowed.ports:
                        for p in allowed.ports:
                            # Trata ranges ou números diretos de porta SSH/RDP
                            if "22" in p or "3389" in p:
                                is_unsafe = True

                if is_unsafe:
                    failed_count += 1
                    report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
                    report["audit_findings"].append({
                        "control_category": "NETWORK_PERIMETER_SSRF",
                        "standard_reference": "CIS GCP 3.6",
                        "control_id": "CIS_GCP_3.6",
                        "control_name": "Block Insecure Management Access",
                        "evaluation_status": "FAILED",
                        "resource_affected": fw.name,
                        "severity_level": "CRITICAL",
                        "finding_details": f"Firewall Rule '{fw.name}' allows direct incoming SSH/RDP connections from the entire public internet.",
                        "remediation_instructions": "Exclua ou altere o bloco 'source_ranges' da regra no Terraform, restringindo-a para o bloco do IAP."
                    })

        report["compliance_summary"]["failed_checks"] = failed_count
        report["compliance_summary"]["passed_checks"] = len(firewalls) - failed_count
        report["compliance_summary"]["compliance_score"] = ((len(firewalls) - failed_count) / len(firewalls)) * 100.0

        print(json.dumps(report, indent=2))
        sys.exit(1 if failed_count > 0 else 0)

    except Exception as e:
        logging.error(f"Error executing audit: {str(e)}")
        print(json.dumps({"status": "ERROR", "message": str(e)}, indent=2))
        sys.exit(2)

if __name__ == "__main__":
    audit_firewall_rules()

# Audit checkpoint [2026-03-16]: feat(audit-logging): configure Cloud Audit Logs streaming to client Splunk SIEM

# Audit checkpoint [2026-04-21]: refactor(org-policy): optimize org policy constraints validator for client multi-tenant storage

# Audit checkpoint [2026-04-22]: feat(audit-logging): configure Cloud Audit Logs streaming to client Splunk SIEM

# Audit checkpoint [2026-05-08]: fix(bucket-retention): fix retention lock validation script for external financial client

# Audit checkpoint [2026-06-25]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone

# Audit checkpoint [2026-06-30]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-07-24]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-07-30]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone
