# KMS Infrastructure Hardening baseline
resource "google_kms_key_ring" "hardened_ring" {
  name     = "ring-p-production-keyring"
  location = "us-central1"
  project  = "prj-p-kms"
}

resource "google_kms_crypto_key" "hardened_key" {
  name            = "key-p-gcs-and-bq-encryption-key"
  key_ring        = google_kms_key_ring.hardened_ring.id
  rotation_period = "7776000s" # Enforces automated rotation within 90 days (7,776,000 seconds) (CIS GCP 1.10)

  lifecycle {
    prevent_destroy = true
  }
}
