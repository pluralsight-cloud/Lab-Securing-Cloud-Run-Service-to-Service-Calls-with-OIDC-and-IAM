provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_service" "service" {
  name     = "oidc-lab-service"
  location = var.region

  template {
    spec {
      containers {
        image = var.image

        env {
          name  = "SERVICE_URL"
          value = ""   
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
