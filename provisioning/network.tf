/*
* Defines network resources, ip allocation mode,
* and firewall rules for control machine
*/

resource "google_compute_network" "zoomcamp_vpc" {
  name                    = "zoomcamp-vpc"
  description             = "DE ZoomCamp default VPC"
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

resource "google_compute_subnetwork" "zoomcamp_subnet" {
  name          = "zoomcamp-subnet"
  ip_cidr_range = var.ip_cidr_range
  network       = google_compute_network.zoomcamp_vpc.id
}

resource "google_compute_firewall" "internal_traffic" {
  name    = "zoomcamp-internal-traffic"
  network = google_compute_network.zoomcamp_vpc.name

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  source_ranges = [var.ip_cidr_range]
}

resource "google_compute_firewall" "allow_web" {
  name    = "zoomcamp-allow-web"
  network = google_compute_network.zoomcamp_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]

  target_tags = ["web"]
}

resource "google_compute_firewall" "allow_ssh" {
  name    = "zoomcamp-allow-ssh"
  network = google_compute_network.zoomcamp_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]

  target_tags = ["ssh"]
}