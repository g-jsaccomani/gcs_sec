# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

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

def audit_vpc_flow_logs():
    report = {
        "audit_metadata": {
            "project_id": "unknown",
            "control_id": "CIS_GCP_4.0.0_3.8",
            "control_name": "VPC Subnet Flow Logging Enablement check",
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
        subnetwork_client = compute_v1.SubnetworksClient(credentials=credentials)
        request = compute_v1.AggregatedListSubnetworksRequest(project=project_id)
        subnets_iterator = subnetwork_client.aggregated_list(request=request)
        
        total_subnets = 0
        failed_subnets = 0

        for region, response in subnets_iterator:
            if response.subnetworks:
                for subnet in response.subnetworks:
                    total_subnets += 1
                    flow_logs_enabled = bool(subnet.enable_flow_logs)

                    if not flow_logs_enabled:
                        failed_subnets += 1
                        report["audit_findings"].append({
                            "control_category": "NETWORK_PERIMETER_SSRF",
                            "standard_reference": "CIS GCP v4.0.0 3.8",
                            "control_id": "CIS_GCP_4.0.0_3.8",
                            "control_name": "Ensure VPC Flow Logs are Enabled",
                            "evaluation_status": "FAILED",
                            "severity_level": "MEDIUM",
                            "resource_affected": subnet.self_link,
                            "finding_details": f"Subnetwork '{subnet.name}' in region '{subnet.region}' has Flow Logging disabled.",
                            "remediation_instructions": "Modify subnetwork settings using Terraform or gcloud to enable flow logs."
                        })
                    else:
                        report["compliance_summary"]["passed_checks"] += 1

        report["compliance_summary"]["total_checks_executed"] = total_subnets
        report["compliance_summary"]["failed_checks"] = failed_subnets
        
        if failed_subnets > 0:
            report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
            report["compliance_summary"]["compliance_score"] = round(((total_subnets - failed_subnets) / total_subnets) * 100, 2)
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
    audit_vpc_flow_logs()

# Audit checkpoint [2025-12-19]: feat(audit-logging): configure Cloud Audit Logs streaming to client Splunk SIEM

# Audit checkpoint [2026-01-21]: refactor(org-policy): optimize org policy constraints validator for client multi-tenant storage
