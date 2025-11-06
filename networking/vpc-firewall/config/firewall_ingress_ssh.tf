# Hardened Firewall Policy rules - Disallowing SSH/RDP global ranges
resource "google_compute_firewall" "allow_iap_ssh" {
  name    = "fw-allow-iap-ssh-ingress"
  network = "vpc-production"
  project = var.project_id

  direction = "INGRESS"
  priority  = 1000

  # Libera acesso apenas para o bloco CIDR oficial do GCP IAP (Identity-Aware Proxy)
  source_ranges = ["35.235.240.0/20"]

  allow {
    protocol = "tcp"
    ports    = ["22", "3389"] # SSH e RDP blindados via IAP
  }
}
