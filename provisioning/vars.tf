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
  default     = "e2-standard-2"
}

variable "disk_size" {
  description = "Machine disk size"
  default     = 50
}

variable "elt_bucket_name" {
  description = "Bucket Name"
  default     = "de-zoomcamp-area"
}

variable "ip_cidr_range" {
  description = "IP CIDR range for the subnetwork"
  default     = "10.20.30.0/24"
}

variable "ssh_username" {
  default = "de_camp"
}