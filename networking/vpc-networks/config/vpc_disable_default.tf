# VPC Infrastructure Hardening and Custom network deployment
resource "google_compute_network" "custom_vpc" {
  name                    = "vpc-production"
  auto_create_subnetworks = false # Avoids default subnet provisioning (CIS GCP 3.1)
  project                 = "prj-net-production-svpc"
}

resource "google_compute_subnetwork" "secure_subnet" {
  name                     = "sub-production-compute"
  ip_cidr_range            = "10.0.1.0/24"
  region                   = "us-central1"
  network                  = google_compute_network.custom_vpc.id
  private_ip_google_access = true # Enables PGA for secure endpoint traffic (CIS GCP 3.2)

  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA" # Enabled VPC Flow Logs (CIS GCP 3.8)
  }
}
