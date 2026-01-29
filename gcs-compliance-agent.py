# Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
# Role: Cloud Security Consultant | LinkedIn: https://www.linkedin.com/in/jsaccomani
# Licensed under the Apache License, Version 2.0.

import sys
import json
import logging
from typing import Dict, List, Any

# pyrefly: ignore [missing-import]
from google.cloud import storage
# pyrefly: ignore [missing-import]
from google.auth import default
# pyrefly: ignore [missing-import]
from google.adk import agents as adk_agents
# pyrefly: ignore [missing-import]
from google.adk import tools as adk_tools

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

@adk_tools.tool
def audit_environment_gcs_posture(env_params_json: str) -> str:
    """
    Evaluates the compliance and hardening posture of Google Cloud Storage buckets based on custom input parameters.
    Supports strictly passive, read-only metadata assessment. Maps to CIS GCP Foundations v4.0.0 (5.1 and 5.2).
    
    Args:
        env_params_json: A JSON-formatted string containing the target GCS environment parameters.
                         Expected Schema:
                         {
                           "target_project": str,
                           "target_buckets": [str],
                           "risk_acceptance": {
                             "exceptions_allowed": bool,
                             "accepted_controls": [
                               {
                                 "control_id": str,
                                 "owner_sign_off": bool,
                                 "owner_email": str,
                                 "justification": str
                               }
                             ]
                           }
                         }
    Returns:
        A JSON string containing the detailed risk audit report and metrics.
    """
    try:
        params = json.loads(env_params_json)
        target_project = params.get("target_project")
        target_buckets = params.get("target_buckets", [])
        risk_config = params.get("risk_acceptance", {})
        exceptions_allowed = risk_config.get("exceptions_allowed", False)
        accepted_controls = risk_config.get("accepted_controls", [])

        # Create mapping of accepted risks for fast lookup
        accepted_map = {}
        for item in accepted_controls:
            if item.get("owner_sign_off") is True:
                accepted_map[item.get("control_id")] = {
                    "owner": item.get("owner_email"),
                    "justification": item.get("justification")
                }

        # Resolve credentials
        credentials, default_project = default()
        project_id = target_project if target_project else default_project
        if not project_id:
            raise ValueError("Target project ID could not be resolved.")

        storage_client = storage.Client(credentials=credentials, project=project_id)
        
        # If no explicit list of buckets is provided, list all buckets passively
        if not target_buckets:
            buckets = list(storage_client.list_buckets())
        else:
            buckets = []
            for b_name in target_buckets:
                try:
                    buckets.append(storage_client.get_bucket(b_name))
                except Exception as e:
                    logging.warning(f"Failed to fetch bucket {b_name} passively: {str(e)}")

        audit_report = {
            "audit_metadata": {
                "project_id": project_id,
                "compliance_agent_version": "5.0.0-disruptive-compliance",
                "one_security_bar_version": "OSB-v4.0"
            },
            "compliance_summary": {
                "overall_status": "COMPLIANT",
                "compliance_score": 100.0,
                "total_checks_executed": 0,
                "passed_checks": 0,
                "failed_checks": 0,
                "risk_accepted_checks": 0
            },
            "audit_findings": []
        }

        total_checks = 0
        passed = 0
        failed = 0
        risk_accepted = 0

        for bucket in buckets:
            bucket.reload()
            
            # ----------------------------------------------------
            # CHECK 1: CIS GCP 5.1 - Public Access Prevention (PAP)
            # ----------------------------------------------------
            total_checks += 1
            pap_state = bucket.public_access_prevention
            pap_compliant = (pap_state == "enforced")
            
            if pap_compliant:
                passed += 1
                status = "PASSED"
                finding_msg = f"Public Access Prevention (PAP) is enforced on bucket '{bucket.name}'."
                accepted_by_po = False
                owner_info = None
                justification_info = None
            else:
                # Evaluate Risk Acceptance
                control_id = "CIS_GCP_v4.0.0_5.1"
                if exceptions_allowed and control_id in accepted_map:
                    risk_accepted += 1
                    status = "RISK_ACCEPTED"
                    finding_msg = (f"Public Access Prevention (PAP) is NOT enforced on bucket '{bucket.name}'. "
                                   f"Status is '{pap_state}'. Non-compliance risk accepted by product owner.")
                    accepted_by_po = True
                    owner_info = accepted_map[control_id]["owner"]
                    justification_info = accepted_map[control_id]["justification"]
                else:
                    failed += 1
                    status = "FAILED"
                    finding_msg = (f"Public Access Prevention (PAP) is NOT enforced on bucket '{bucket.name}'. "
                                   f"Current status is '{pap_state}'.")
                    accepted_by_po = False
                    owner_info = None
                    justification_info = None

            audit_report["audit_findings"].append({
                "control_category": "NETWORK_PERIMETER_SSRF",
                "standard_reference": "CIS GCP Foundations Benchmark v4.0.0 (5.1)",
                "control_id": "CIS_GCP_v4.0.0_5.1",
                "control_name": "Public Access Prevention on GCS Buckets",
                "evaluation_status": status,
                "severity_level": "CRITICAL" if status == "FAILED" else "INFORMATIONAL",
                "resource_affected": bucket.self_link,
                "finding_details": finding_msg,
                "risk_acceptance_metadata": {
                    "accepted_by_product_owner": accepted_by_po,
                    "approved_by_email": owner_info,
                    "business_justification": justification_info
                }
            })

            # ----------------------------------------------------
            # CHECK 2: CIS GCP 5.2 - Uniform Bucket-Level Access (UBLA)
            # ----------------------------------------------------
            total_checks += 1
            ubla_enabled = bucket.iam_configuration.uniform_bucket_level_access.enabled
            
            if ubla_enabled:
                passed += 1
                status = "PASSED"
                finding_msg = f"Uniform Bucket-Level Access is enabled on bucket '{bucket.name}'."
                accepted_by_po = False
                owner_info = None
                justification_info = None
            else:
                # Evaluate Risk Acceptance
                control_id = "CIS_GCP_v4.0.0_5.2"
                if exceptions_allowed and control_id in accepted_map:
                    risk_accepted += 1
                    status = "RISK_ACCEPTED"
                    finding_msg = (f"Uniform Bucket-Level Access is disabled on bucket '{bucket.name}'. "
                                   f"Non-compliance risk accepted by product owner.")
                    accepted_by_po = True
                    owner_info = accepted_map[control_id]["owner"]
                    justification_info = accepted_map[control_id]["justification"]
                else:
                    failed += 1
                    status = "FAILED"
                    finding_msg = f"Uniform Bucket-Level Access is disabled on bucket '{bucket.name}'."
                    accepted_by_po = False
                    owner_info = None
                    justification_info = None

            audit_report["audit_findings"].append({
                "control_category": "IDENTITY_AUTH_IAM",
                "standard_reference": "CIS GCP Foundations Benchmark v4.0.0 (5.2)",
                "control_id": "CIS_GCP_v4.0.0_5.2",
                "control_name": "Uniform Bucket-Level Access on GCS Buckets",
                "evaluation_status": status,
                "severity_level": "HIGH" if status == "FAILED" else "INFORMATIONAL",
                "resource_affected": bucket.self_link,
                "finding_details": finding_msg,
                "risk_acceptance_metadata": {
                    "accepted_by_product_owner": accepted_by_po,
                    "approved_by_email": owner_info,
                    "business_justification": justification_info
                }
            })

        # Calculations
        audit_report["compliance_summary"]["total_checks_executed"] = total_checks
        audit_report["compliance_summary"]["passed_checks"] = passed
        audit_report["compliance_summary"]["failed_checks"] = failed
        audit_report["compliance_summary"]["risk_accepted_checks"] = risk_accepted

        # Math score: (passed + risk_accepted) / total_checks
        if total_checks > 0:
            score = ((passed + risk_accepted) / total_checks) * 100
            audit_report["compliance_summary"]["compliance_score"] = round(score, 2)
        else:
            audit_report["compliance_summary"]["compliance_score"] = 100.0

        if failed > 0:
            audit_report["compliance_summary"]["overall_status"] = "NON_COMPLIANT"
        elif risk_accepted > 0:
            audit_report["compliance_summary"]["overall_status"] = "COMPLIANT_WITH_EXCEPTIONS"
        else:
            audit_report["compliance_summary"]["overall_status"] = "COMPLIANT"

        return json.dumps(audit_report, indent=2)

    except Exception as e:
        error_res = {
            "status": "ERROR",
            "error_details": str(e)
        }
        return json.dumps(error_res, indent=2)

# Define target LLM Agent
gcs_compliance_agent = adk_agents.LlmAgent(
    model="gemini-2.5-flash",
    name="gcs_disruptive_compliance_specialist",
    description="Custom disruptive agent that ingests target GCS environment parameters, runs strict passive auditing, "
                "evaluates risk metrics, and supports Owner risk acceptance mapping.",
    instruction="""
    INSTRUCTIONS:
    You are the Lead GCS Compliance & Hardening Specialist Agent.
    1. Always act strictly as a passive auditor. Perform no mutating or configuration change operations.
    2. When asked to evaluate an environment's GCS hardening, prompt the user or construct a JSON payload for the tool 'audit_environment_gcs_posture' with the target environment parameters (target_project, target_buckets, risk_acceptance).
    3. If any controls fail, check if the Product Owner ('owner') has signed off ('owner_sign_off' = True) on the specific control in the 'risk_acceptance' payload. 
    4. If signed off, evaluate the finding status as 'RISK_ACCEPTED' and include the justification in the compliance summary. Do not count this as an active failure in the compliance score.
    5. Always output the final report in clean structured Markdown or raw JSON as requested, showing the compliance metrics clearly.
    """,
    tools=[audit_environment_gcs_posture]
)

# Audit checkpoint [2026-01-29]: fix(bucket-retention): fix retention lock validation script for external financial client
