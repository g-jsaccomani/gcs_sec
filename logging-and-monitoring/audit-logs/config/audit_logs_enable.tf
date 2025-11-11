# Organization Audit Logging baseline config
resource "google_project_iam_audit_config" "audit_config" {
  project = "prj-p-workload"
  service = "allServices" # Configures logging globally across all API endpoints (CIS GCP 2.1)

  audit_log_config {
    log_type = "DATA_READ" # Tracks read activities on data tables and storage objects
  }

  audit_log_config {
    log_type = "DATA_WRITE" # Tracks any creation, edit, or delete action on datasets
  }

  audit_log_config {
    log_type = "ADMIN_READ" # Tracks administrative API configs
  }
}
