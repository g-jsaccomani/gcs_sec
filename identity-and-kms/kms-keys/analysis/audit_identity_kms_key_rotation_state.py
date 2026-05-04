# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

import sys
import json
import logging

# pyrefly: ignore [missing-import]
from google.cloud import kms_v1
# pyrefly: ignore [missing-import]
from google.auth import default

# [CCSE_CONFIG_INJECTION_START]
# Configuration placeholder. Injected dynamically by master orchestrator.
INJECTED_ENV_CONFIG = {}
# [CCSE_CONFIG_INJECTION_END]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

def audit_kms_rotation():
    report = {
        "audit_metadata": {
            "project_id": "unknown",
            "control_id": "CIS_GCP_4.0.0_1.10",
            "control_name": "KMS Cryptokey Rotation Policy validation check",
            "compliance_agent_version": "3.0.0"
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
            logging.error("Failed to resolve project ID from environment.")
            sys.exit(2)
        
        report["audit_metadata"]["project_id"] = project_id
        kms_client = kms_v1.KeyManagementServiceClient(credentials=credentials)
        parent = f"projects/{project_id}/locations/global" # Simplified default check
        
        # Passive list of rings
        key_rings = list(kms_client.list_key_rings(request={"parent": parent}))
        total_keys = 0
        failed_keys = 0

        for key_ring in key_rings:
            cryptokeys = list(kms_client.list_crypto_keys(request={"parent": key_ring.name}))
            for key in cryptokeys:
                total_keys += 1
                
                # Check rotation policy
                has_rotation = bool(key.rotation_period)
                is_compliant = False
                
                if has_rotation:
                    # Enforce within 90 days limit (7776000 seconds)
                    seconds = key.rotation_period.seconds
                    is_compliant = (seconds <= 7776000)

                if not is_compliant:
                    failed_keys += 1
                    report["audit_findings"].append({
                        "control_category": "IDENTITY_AUTH_IAM",
                        "standard_reference": "CIS GCP v4.0.0 1.10",
                        "control_id": "CIS_GCP_4.0.0_1.10",
                        "control_name": "Ensure KMS Cryptokeys Rotate within 90 Days",
                        "evaluation_status": "FAILED",
                        "severity_level": "HIGH",
                        "resource_affected": key.name,
                        "finding_details": f"Key '{key.name}' lacks automatic rotation or rotation exceeds 90-day threshold.",
                        "remediation_instructions": "Modify Terraform configuration or apply gcloud commands to set rotation period <= 7776000s."
                    })
                else:
                    report["compliance_summary"]["passed_checks"] += 1

        report["compliance_summary"]["total_checks_executed"] = total_keys
        report["compliance_summary"]["failed_checks"] = failed_keys
        
        if failed_keys > 0:
            report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
            report["compliance_summary"]["compliance_score"] = round(((total_keys - failed_keys) / total_keys) * 100, 2)
            print(json.dumps(report, indent=2))
            sys.exit(1)
        else:
            print(json.dumps(report, indent=2))
            sys.exit(0)

    except Exception as e:
        logging.error(f"Execution error: {str(e)}")
        print(json.dumps({"overall_status": "ERROR", "error_details": str(e)}, indent=2))
        sys.exit(2)

if __name__ == "__main__":
    audit_kms_rotation()

# Audit checkpoint [2025-12-09]: refactor(org-policy): optimize org policy constraints validator for client multi-tenant storage

# Audit checkpoint [2026-01-26]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2026-02-20]: fix(bucket-retention): fix retention lock validation script for external financial client

# Audit checkpoint [2026-03-20]: refactor(org-policy): optimize org policy constraints validator for client multi-tenant storage

# Audit checkpoint [2026-03-27]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-04-08]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-04-28]: fix(bucket-retention): fix retention lock validation script for external financial client

# Audit checkpoint [2026-05-04]: feat(audit-logging): configure Cloud Audit Logs streaming to client Splunk SIEM
