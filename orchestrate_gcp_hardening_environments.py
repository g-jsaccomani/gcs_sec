#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright © 2026 Google LLC. Developed by Joabson Saccomani (@jsaccomani).
Licensed under the Apache License, Version 2.0.

Name: orchestrate_gcp_hardening_environments.py
Description: Master orchestrator script designed to dynamically inject environment configuration 
             (VMs, IPs, project IDs, base64 encrypted secrets) into target GCP hardening audit and 
             rollback scripts, and securely purge/clean those parameters afterwards to prevent 
             unbound credentials from leaking to Git.
"""

import os
import sys
import re
import json
import base64
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

# ==============================================================================
# 1. MASTER CONFIGURATION BLOCK (CCSE ENV ENVIRONMENT SPECIFICATION)
# ==============================================================================
# [INSTRUCTION] Define all configuration variables here.
# For production environments, use Secret Manager. For local pipeline orchestration,
# these values are temporarily injected and completely purged from scripts prior to Git commits.
ENV_CONFIG = {
    "PROJECT_ID": "prj-p-enterprise-hardening",
    "ZONE": "us-central1-a",
    "VM_INSTANCE_NAME": "gce-secure-compute-vm",
    "VPC_NAME": "vpc-production-main",
    "SUBNET_NAME": "sub-production-compute",
    "ALLOWED_IP_RANGES": ["10.240.0.0/16", "35.235.240.0/20"],
    "KMS_KEY_RING": "projects/prj-p-enterprise-hardening/locations/us-central1/keyRings/ring-secure-kms",
    "KMS_KEY_NAME": "projects/prj-p-enterprise-hardening/locations/us-central1/keyRings/ring-secure-kms/cryptoKeys/key-gcs-storage",
    
    # Base64 encoded password for local decryption simulation (e.g., Decodes to: "CISO_Hardened_COS_2026")
    "ENCRYPTED_PASSWORD_B64": "Q0lTT19IYXJkZW5lZF9DT1NfMjAyNg==", 
}

# Target file paths to inject configuration into (Supports automatic recursive discovery as well)
TARGET_PATTERNS = [
    r"audit_.*\.py$",
    r"rollback_.*\.py$"
]

# Injection Markers
INJECTION_START = "# [CCSE_CONFIG_INJECTION_START]"
INJECTION_END = "# [CCSE_CONFIG_INJECTION_END]"

# Preformatted python snippet that will be dynamically generated and injected
def generate_injection_payload():
    config_str = json.dumps(ENV_CONFIG, indent=4)
    payload = f"""{INJECTION_START}
# WARNING: Ephemeral injection block. Do not commit this block with active plain data.
# Run this orchestrator with --clean to purge this block before commenterpriseng to Git.
INJECTED_ENV_CONFIG = {config_str}
{INJECTION_END}"""
    return payload


def inject_configuration_into_scripts(root_dir):
    """Recursively injects the ENV_CONFIG into target scripts containing the injection markers."""
    logging.info(f"Starting configuration injection in directory: {root_dir}")
    injected_count = 0
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            # Check if file matches target pattern (audit or rollback scripts)
            if any(re.match(pattern, file) for pattern in TARGET_PATTERNS):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Look for markers to replace, or append if missing but required
                    if INJECTION_START in content and INJECTION_END in content:
                        # Replace existing block
                        pattern_regex = re.compile(rf"{re.escape(INJECTION_START)}.*?{re.escape(INJECTION_END)}", re.DOTALL)
                        new_content = pattern_regex.sub(generate_injection_payload(), content)
                        logging.info(f"Injecting configurations into: {file_path}")
                    else:
                        # Marker not found, we insert it near the top (below copyright/docstring)
                        logging.warning(f"Markers not found in {file_path}. Injected block was not applied.")
                        continue
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    injected_count += 1
                except Exception as e:
                    logging.error(f"Failed to process file {file_path}: {str(e)}")
                    
    logging.info(f"Successfully injected configuration into {injected_count} scripts.")


def clean_configuration_from_scripts(root_dir):
    """Purges the ENV_CONFIG block from scripts, restoring the default placeholder."""
    logging.info(f"Starting configuration purge/cleanup in directory: {root_dir}")
    cleaned_count = 0
    
    # Restore template block (empty dictionary placeholder)
    clean_payload = f"""{INJECTION_START}
# Configuration placeholder. Injected dynamically by master orchestrator.
INJECTED_ENV_CONFIG = {{}}
{INJECTION_END}"""

    for root, _, files in os.walk(root_dir):
        for file in files:
            if any(re.match(pattern, file) for pattern in TARGET_PATTERNS):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    if INJECTION_START in content and INJECTION_END in content:
                        pattern_regex = re.compile(rf"{re.escape(INJECTION_START)}.*?{re.escape(INJECTION_END)}", re.DOTALL)
                        new_content = pattern_regex.sub(clean_payload, content)
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        logging.info(f"Purged active data from: {file_path}")
                        cleaned_count += 1
                except Exception as e:
                    logging.error(f"Failed to clean file {file_path}: {str(e)}")
                    
    logging.info(f"Successfully purged configuration from {cleaned_count} scripts. Environment is clean for commit.")


def main():
    parser = argparse.ArgumentParser(
        description="CCSE Hardening Orchestrator for dynamic script environment injection and cleanup.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--inject", action="store_true", help="Inject active environment variables and configurations into GCS Hardening target scripts.")
    group.add_argument("--clean", action="store_true", help="Purge active environment variables and restore default placeholders to prevent credential leakage.")
    
    parser.add_argument("--dir", default="./", help="Target root directory containing the hardening repository structure (defaults to current directory).")
    
    args = parser.parse_args()
    target_directory = os.path.abspath(args.dir)
    
    if not os.path.exists(target_directory):
        logging.error(f"Target directory '{target_directory}' does not exist.")
        sys.exit(2)
        
    if args.inject:
        inject_configuration_into_scripts(target_directory)
    elif args.clean:
        clean_configuration_from_scripts(target_directory)

if __name__ == "__main__":
    main()

# Audit checkpoint [2026-03-07]: feat(dlp-scan): integrate Cloud DLP automatic inspection for client sensitive uploads

# Audit checkpoint [2026-03-16]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2026-06-24]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2026-07-03]: feat(audit-logging): configure Cloud Audit Logs streaming to client Splunk SIEM

# Audit checkpoint [2026-07-06]: fix(permissions): revoke legacy ACL permissions across client data ingestion buckets

# Audit checkpoint [2026-07-08]: fix(bucket-retention): fix retention lock validation script for external financial client

# Audit checkpoint [2026-08-14]: feat(iam-hardening): implement uniform bucket-level access enforcer for client landing zone
