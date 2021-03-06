/*
* Defines mais resources used in Data Engineering ZoomCamp
*
*/

provider "google" {
  project = var.project
  region  = var.region
}


/*
* Remote machine that serves Airflow
*/
resource "google_compute_instance" "control_machine" {
  name                      = "de-control-machine"
  machine_type              = var.machine_type
  tags                      = ["web", "ssh"]
  zone                      = var.zone
  allow_stopping_for_update = true

  network_interface {
    subnetwork = google_compute_subnetwork.zoomcamp_subnet.name

    access_config {
      // Ephemeral public IP
    }
  }

  boot_disk {
    initialize_params {
      image = var.vm_image
      size  = var.disk_size
      type  = "pd-ssd"
    }
  }

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = var.control_machine_svc_acc
    scopes = ["cloud-platform"]
  }
}

/*
* Storage area for parquet files
*/
resource "google_storage_bucket" "elt_bucket" {
  name                        = var.elt_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
}