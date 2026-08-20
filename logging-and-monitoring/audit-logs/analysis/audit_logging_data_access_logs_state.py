# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

import sys
import json
import logging

# pyrefly: ignore [missing-import]
from google.cloud import resourcemanager_v3
# pyrefly: ignore [missing-import]
from google.auth import default

# [CCSE_CONFIG_INJECTION_START]
# Configuration placeholder. Injected dynamically by master orchestrator.
INJECTED_ENV_CONFIG = {}
# [CCSE_CONFIG_INJECTION_END]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

def audit_project_audit_logs():
    report = {
        "audit_metadata": {
            "project_id": "unknown",
            "control_id": "CIS_GCP_4.0.0_2.1",
            "control_name": "GCP Data Access Logs configuration check",
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
        rm_client = resourcemanager_v3.ProjectsClient(credentials=credentials)
        project_name = f"projects/{project_id}"
        
        # Read the IAM policy of the project (strictly passive)
        policy = rm_client.get_iam_policy(resource=project_name)
        
        has_all_services_config = False
        data_read_enabled = False
        data_write_enabled = False

        if policy.audit_configs:
            for audit_config in policy.audit_configs:
                if audit_config.service == "allServices":
                    has_all_services_config = True
                    for log_config in audit_config.audit_log_configs:
                        if log_config.log_type == "DATA_READ":
                            data_read_enabled = True
                        if log_config.log_type == "DATA_WRITE":
                            data_write_enabled = True

        is_compliant = has_all_services_config and data_read_enabled and data_write_enabled
        report["compliance_summary"]["total_checks_executed"] = 1

        if not is_compliant:
            report["compliance_summary"]["failed_checks"] = 1
            report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
            report["compliance_summary"]["compliance_score"] = 0.0
            report["audit_findings"].append({
                "control_category": "TELEMETRY_HELM_OSLO",
                "standard_reference": "CIS GCP v4.0.0 2.1",
                "control_id": "CIS_GCP_4.0.0_2.1",
                "control_name": "Configure Data Access Logging Globally",
                "evaluation_status": "FAILED",
                "severity_level": "HIGH",
                "resource_affected": project_name,
                "finding_details": f"Project '{project_id}' does not have allServices audit logs configured with DATA_READ and DATA_WRITE.",
                "remediation_instructions": "Deploy audit_logs_enable.tf configuration using Terraform to restore global Logging compliance."
            })
        else:
            report["compliance_summary"]["passed_checks"] = 1

        if not is_compliant:
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
    audit_project_audit_logs()

# Audit checkpoint [2025-12-08]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2025-12-14]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2025-12-30]: fix(bucket-retention): fix retention lock validation script for external financial client

# Audit checkpoint [2026-01-12]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone

# Audit checkpoint [2026-05-06]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone

# Audit checkpoint [2026-05-11]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-06-06]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2026-07-07]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone

# Audit checkpoint [2026-07-16]: fix(bucket-retention): fix retention lock validation script for external financial client

# Audit checkpoint [2026-08-17]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-08-20]: fix(bucket-retention): fix retention lock validation script for external financial client
