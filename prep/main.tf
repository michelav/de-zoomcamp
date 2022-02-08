variable "project" {
  description = "GCP project ID"
}

variable "region" {
  description = "GCP Region"
  default     = "southamerica-west1"
}

variable "zone" {
  description = "GCP Zone"
  default     = "southamerica-west1-a"
}

variable "vm_image" {
  description = "SO Image to be used"
}

variable "control_machine_svc_acc" {
  description = "Service Account e-mail to be set in GCS VM"
}

variable "machine_type" {
  description = "Machine specs to be used"
  default = "e2-standard-2"
}

variable "elt_bucket_name" {
  description = "Bucket Name"
  default = "de-zoomcamp-area"
}

provider "google" {
  project     = var.project
  region      = var.region
}

resource "google_compute_instance" "control_machine" {
  name                      = "de-control-machine"
  machine_type              = var.machine_type
  tags                      = ["tf-created", "de-zoomcamp"]
  zone                      = var.zone
  allow_stopping_for_update = true

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }

  boot_disk {
    initialize_params {
      image = var.vm_image
      size  = 20
      type  = "pd-ssd"
    }
  }

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = var.control_machine_svc_acc
    scopes = ["cloud-platform"]
  }
}

resource "google_storage_bucket" "elt_bucket" {
  name                        = var.elt_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
}

output "control_machine_address" {
  description = "Control Machine IP"
  value       = google_compute_instance.control_machine.network_interface.0.access_config.0.nat_ip
}