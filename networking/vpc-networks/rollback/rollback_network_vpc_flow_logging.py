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

def rollback_vpc_flow_logging():
    output = {
        "rollback_metadata": {
            "target_control": "CIS_GCP_4.0.0_3.8",
            "control_name": "VPC Flow Logging",
            "execution_developer": "@jsaccomani"
        },
        "rollback_summary": {
            "status": "PENDING",
            "affected_resources": []
        }
    }

    try:
        credentials, project_id = default()
        if not project_id:
            logging.error("GCP Project ID could not be resolved from environment.")
            sys.exit(2)

        subnetworks_client = compute_v1.SubnetworksClient(credentials=credentials)
        regions_client = compute_v1.RegionsClient(credentials=credentials)

        regions = regions_client.list(project=project_id)
        
        for region in regions:
            subnets = subnetworks_client.list(project=project_id, region=region.name)
            for subnet in subnets:
                if subnet.enable_flow_logs:
                    subnet_resource = compute_v1.Subnetwork(
                        enable_flow_logs=False,
                        fingerprint=subnet.fingerprint
                    )
                    operation = subnetworks_client.patch(
                        project=project_id,
                        region=region.name,
                        subnetwork=subnet.name,
                        subnetwork_resource=subnet_resource
                    )
                    output["rollback_summary"]["affected_resources"].append({
                        "resource_type": "subnetwork",
                        "resource_id": subnet.self_link,
                        "property_reverted": "enable_flow_logs=False"
                    })

        output["rollback_summary"]["status"] = "SUCCESS"
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except Exception as e:
        logging.error(f"Rollback execution failed: {str(e)}")
        output["rollback_summary"]["status"] = "FAILED"
        output["rollback_summary"]["error_message"] = str(e)
        print(json.dumps(output, indent=2))
        sys.exit(2)

if __name__ == "__main__":
    rollback_vpc_flow_logging()

# Audit checkpoint [2026-02-15]: fix(bucket-retention): fix retention lock validation script for external financial client

# Audit checkpoint [2026-02-15]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-05-11]: refactor(org-policy): optimize org policy constraints validator for client multi-tenant storage

# Audit checkpoint [2026-07-01]: refactor(org-policy): optimize org policy constraints validator for client multi-tenant storage

# Audit checkpoint [2026-07-22]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2026-07-27]: refactor(org-policy): optimize org policy constraints validator for client multi-tenant storage
