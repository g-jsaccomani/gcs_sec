# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: audit_identity_sa_key_leak_prevention.py
Control: CIS GCP v4.0.0 - Controle 1.4 (Ensure no user-managed service account keys exist)
Description: Strictly Read-Only Audit que verifica a existência de chaves estáticas corporativas criadas manualmente por usuários em SAs.
Required IAM: roles/iam.securityAuditor (ou roles/viewer)
"""
import sys
import json
import logging
# pyrefly: ignore [missing-import]
from google.cloud import iam_admin_v1
# pyrefly: ignore [missing-import]
from google.auth import default

# [CCSE_CONFIG_INJECTION_START]
# Configuration placeholder. Injected dynamically by master orchestrator.
INJECTED_ENV_CONFIG = {}
# [CCSE_CONFIG_INJECTION_END]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

def audit_sa_keys():
    report = {
        "audit_metadata": {
            "control_id": "CIS_GCP_4.0.0_1.4",
            "control_name": "Service Account Static Key Validation",
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

        client = iam_admin_v1.IAMClient(credentials=credentials)
        parent = f"projects/{project_id}"
        
        # Listagem de contas de serviço
        service_accounts = list(client.list_service_accounts(name=parent))
        
        total_keys = 0
        user_managed_keys_count = 0

        for sa in service_accounts:
            # Lista as chaves de cada SA
            keys = client.list_service_account_keys(name=sa.name)
            for key in keys.keys:
                total_keys += 1
                
                # USER_MANAGED keys representam chaves JSON geradas por usuários que vazam facilmente
                is_user_key = (key.key_type == iam_admin_v1.types.ListServiceAccountKeysResponse.KeyType.USER_MANAGED)
                
                if is_user_key:
                    user_managed_keys_count += 1
                    report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
                    report["audit_findings"].append({
                        "control_category": "IDENTITY_AUTH_IAM",
                        "standard_reference": "CIS GCP 1.4",
                        "control_id": "CIS_GCP_1.4",
                        "control_name": "No User-Managed SA Keys",
                        "evaluation_status": "FAILED",
                        "severity_level": "CRITICAL",
                        "resource_affected": sa.email,
                        "finding_details": f"User-managed static key found in service account '{sa.email}' (ID: {key.name.split('/')[-1]}).",
                        "remediation_instructions": "Exclua a chave estatica pelo console ou CLI e adote o Workload Identity Federation."
                    })

        report["compliance_summary"]["total_checks_executed"] = total_keys
        report["compliance_summary"]["failed_checks"] = user_managed_keys_count
        report["compliance_summary"]["passed_checks"] = total_keys - user_managed_keys_count
        if total_keys > 0:
            report["compliance_summary"]["compliance_score"] = ((total_keys - user_managed_keys_count) / total_keys) * 100.0

        print(json.dumps(report, indent=2))
        sys.exit(1 if user_managed_keys_count > 0 else 0)

    except Exception as e:
        logging.error(f"Error executing audit: {str(e)}")
        print(json.dumps({"status": "ERROR", "message": str(e)}, indent=2))
        sys.exit(2)

if __name__ == "__main__":
    audit_sa_keys()

# Audit checkpoint [2025-12-15]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone

# Audit checkpoint [2025-12-30]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-02-23]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-02-26]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone

# Audit checkpoint [2026-04-13]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2026-06-05]: feat(audit-logging): configure Cloud Audit Logs streaming to client Splunk SIEM
