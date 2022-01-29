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

variable "machine_type" {
  description = "Machine specs to be used"
  default = "e2-standard-2"
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
}

output "control_machine_address" {
  description = "Control Machine IP"
  value       = google_compute_instance.control_machine.network_interface.0.access_config.0.nat_ip
}