# GKE Hardening - Dataplane V2, Secure Boot and Workload Identity
resource "google_container_cluster" "hardened_cluster" {
  name     = "prj-p-secure-gke-cluster"
  location = "us-central1-a"

  # Enforces Dataplane V2 para Zero-Trust Networking
  datapath_provider = "ADVANCED_DATAPATH"

  # Habilita Workload Identity para eliminar chaves estáticas de SAs (CIS GKE 5.2)
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Habilita Binary Authorization (CIS GKE 5.1)
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  node_config {
    image_type   = "COS_CONTAINERD" # Container-Optimized OS (CIS COS 1.2)
    service_account = google_service_account.gke_sa.email

    shielded_instance_config {
      enable_secure_boot          = true # Secure Boot habilitado para os nós (CIS GCP 4.8)
      enable_integrity_monitoring = true
    }
  }
}
