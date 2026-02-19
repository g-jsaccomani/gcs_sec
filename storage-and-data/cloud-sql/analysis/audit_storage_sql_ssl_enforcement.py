# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: audit_storage_sql_ssl_enforcement.py
Control: CIS GCP v4.0.0 - Controle 6.4 (Ensure Cloud SQL Database instances require SSL connections)
Description: Strictly Read-Only Audit de conexões TLS/SSL ativas em todas as instâncias Cloud SQL do projeto.
Required IAM: roles/cloudsql.viewer
"""
import sys
import json
import logging
# pyrefly: ignore [missing-import]
from google.cloud import sql_v1
# pyrefly: ignore [missing-import]
from google.auth import default

# [CCSE_CONFIG_INJECTION_START]
# Configuration placeholder. Injected dynamically by master orchestrator.
INJECTED_ENV_CONFIG = {}
# [CCSE_CONFIG_INJECTION_END]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

def audit_sql_ssl():
    report = {
        "audit_metadata": {
            "control_id": "CIS_GCP_4.0.0_6.4",
            "control_name": "SQL SSL Enforcement Check",
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

        client = sql_v1.SqlInstancesServiceClient(credentials=credentials)
        request = sql_v1.SqlInstancesListRequest(project=project_id)
        result = client.list(request=request)
        
        instances = list(result.items) if result.items else []
        report["compliance_summary"]["total_checks_executed"] = len(instances)

        if len(instances) == 0:
            print(json.dumps(report, indent=2))
            sys.exit(0)

        failed_count = 0
        for inst in instances:
            # Verifies if require_ssl is active in the control interface
            require_ssl = False
            if inst.settings and inst.settings.ip_configuration:
                require_ssl = inst.settings.ip_configuration.require_ssl

            if not require_ssl:
                failed_count += 1
                report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
                report["audit_findings"].append({
                    "control_category": "NETWORK_PERIMETER_SSRF",
                    "standard_reference": "CIS GCP 6.4",
                    "control_id": "CIS_GCP_6.4",
                    "control_name": "Mandatory SQL SSL Connections",
                    "evaluation_status": "FAILED",
                    "severity_level": "HIGH",
                    "resource_affected": inst.name,
                    "finding_details": f"Database instance '{inst.name}' allows raw unencrypted queries (require_ssl is FALSE).",
                    "remediation_instructions": "Set the 'require_ssl = true' parameter in the Cloud SQL ip_configuration block."
                })

        report["compliance_summary"]["failed_checks"] = failed_count
        report["compliance_summary"]["passed_checks"] = len(instances) - failed_count
        report["compliance_summary"]["compliance_score"] = ((len(instances) - failed_count) / len(instances)) * 100.0

        print(json.dumps(report, indent=2))
        sys.exit(1 if failed_count > 0 else 0)

    except Exception as e:
        logging.error(f"Error executing audit: {str(e)}")
        print(json.dumps({"status": "ERROR", "message": str(e)}, indent=2))
        sys.exit(2)

if __name__ == "__main__":
    audit_sql_ssl()

# Audit checkpoint [2025-12-17]: fix(bucket-retention): fix retention lock validation script for external financial client

# Audit checkpoint [2026-01-11]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2026-01-26]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone

# Audit checkpoint [2026-02-19]: feat(audit-logging): configure Cloud Audit Logs streaming to client Splunk SIEM
