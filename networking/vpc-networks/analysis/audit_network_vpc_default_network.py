# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: audit_network_vpc_default_network.py
Control: CIS GCP v4.0.0 - Controle 3.1 / 3.2 (Ensure default network does not exist)
Description: Garante que nenhuma rede nomeada 'default' existe no projeto, prevenindo implantações inseguras.
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

def audit_default_vpc():
    report = {
        "audit_metadata": {
            "control_id": "CIS_GCP_4.0.0_3.1",
            "control_name": "Check Default Network Existence",
            "compliance_agent_version": "2.4.0",
        },
        "compliance_summary": {
            "overall_status": "COMPLIANT",
            "compliance_score": 100.0,
            "total_checks_executed": 1,
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

        client = compute_v1.NetworksClient(credentials=credentials)
        networks = list(client.list(project=project_id))
        
        has_default = False
        for net in networks:
            if net.name == "default":
                has_default = True

        if has_default:
            report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
            report["compliance_summary"]["failed_checks"] = 1
            report["compliance_summary"]["compliance_score"] = 0.0
            report["audit_findings"].append({
                "control_category": "NETWORK_PERIMETER_SSRF",
                "standard_reference": "CIS GCP 3.1",
                "control_id": "CIS_GCP_3.1",
                "control_name": "No Default Network",
                "evaluation_status": "FAILED",
                "severity_level": "HIGH",
                "resource_affected": "network/default",
                "finding_details": "The default GNET network is still active in this project.",
                "remediation_instructions": "Deleta a rede 'default' e suas regras de firewall padrão utilizando a gcloud CLI ou console."
            })
        else:
            report["compliance_summary"]["passed_checks"] = 1

        print(json.dumps(report, indent=2))
        sys.exit(1 if has_default else 0)

    except Exception as e:
        logging.error(f"Error executing audit: {str(e)}")
        print(json.dumps({"status": "ERROR", "message": str(e)}, indent=2))
        sys.exit(2)

if __name__ == "__main__":
    audit_default_vpc()

# Audit checkpoint [2025-12-03]: feat(audit-logging): configure Cloud Audit Logs streaming to client Splunk SIEM
