# Organization policy block preventing external SA key creation
resource "google_project_organization_policy" "deny_sa_key_creation" {
  project    = var.project_id
  constraint = "constraints/iam.disableServiceAccountKeyCreation" # Organizes prevention against external static key sprawl (CIS GCP 1.4)

  boolean_policy {
    enforced = true
  }
}
