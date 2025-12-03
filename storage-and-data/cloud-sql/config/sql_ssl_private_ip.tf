# Cloud SQL Database Hardening - Private IP, Mandatory SSL, Backups
resource "google_sql_database_instance" "secure_sql_instance" {
  name             = "prj-p-secure-postgresql"
  database_version = "POSTGRES_15"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"

    # Enforce de IP Privado - Sem IPs externos whitelist (CIS GCP 6.5)
    ip_configuration {
      ipv4_enabled    = false
      private_network = "projects/prj-net-production-svpc/global/networks/vpc-production"
      require_ssl     = true # Criptografia obrigatoria em transito (CIS GCP 6.4)
    }

    # Resiliência de Backups automatizados (CIS GCP 6.7)
    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}
